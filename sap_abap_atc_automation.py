#!/usr/bin/env python3
"""
SAP ABAP ATC Check Automation Tool
Automatically fixes Open SQL syntax errors in restricted language scope
for ABAP_CLOUD_READINESS compliance.
"""

import os
import re
import json
import logging
from datetime import datetime
from typing import List, Dict, Tuple, Optional
import xml.etree.ElementTree as ET

class SAPABAPATCAutomation:
    def __init__(self, config_file: str = "atc_config.json"):
        """Initialize the ATC automation tool."""
        self.config = self.load_config(config_file)
        self.setup_logging()
        self.fixes_applied = 0
        self.errors_fixed = 0
        
    def setup_logging(self):
        """Setup logging configuration."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('atc_automation.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def load_config(self, config_file: str) -> Dict:
        """Load configuration from JSON file."""
        default_config = {
            "backup_enabled": True,
            "backup_directory": "backups",
            "max_backups": 10,
            "fix_patterns": {
                "open_sql_syntax": [
                    r"SELECT\s+.*\s+FROM\s+.*\s+WHERE\s+.*",
                    r"INSERT\s+INTO\s+.*\s+VALUES\s+.*",
                    r"UPDATE\s+.*\s+SET\s+.*\s+WHERE\s+.*",
                    r"DELETE\s+FROM\s+.*\s+WHERE\s+.*"
                ],
                "restricted_language": [
                    r"COMMIT\s+WORK",
                    r"ROLLBACK\s+WORK",
                    r"SY-SUBRC\s*=",
                    r"SY-DBCNT\s*="
                ]
            },
            "replacement_patterns": {
                "open_sql_syntax": {
                    "SELECT": "SELECT_SINGLE",
                    "INSERT": "INSERT_INTO",
                    "UPDATE": "UPDATE_FROM",
                    "DELETE": "DELETE_FROM"
                },
                "restricted_language": {
                    "COMMIT WORK": "COMMIT WORK AND WAIT",
                    "ROLLBACK WORK": "ROLLBACK WORK AND WAIT",
                    "SY-SUBRC =": "IF sy-subrc <> 0",
                    "SY-DBCNT =": "IF sy-dbcnt > 0"
                }
            }
        }
        
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r') as f:
                    user_config = json.load(f)
                    default_config.update(user_config)
            except Exception as e:
                self.logger.warning(f"Error loading config: {e}, using defaults")
                
        return default_config
        
    def create_backup(self, file_path: str) -> str:
        """Create backup of the original file."""
        if not self.config["backup_enabled"]:
            return file_path
            
        backup_dir = self.config["backup_directory"]
        os.makedirs(backup_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.basename(file_path)
        backup_path = os.path.join(backup_dir, f"{filename}.{timestamp}.bak")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as src:
                with open(backup_path, 'w', encoding='utf-8') as dst:
                    dst.write(src.read())
            self.logger.info(f"Backup created: {backup_path}")
            return backup_path
        except Exception as e:
            self.logger.error(f"Backup failed: {e}")
            return file_path
            
    def analyze_atc_results(self, atc_xml_file: str) -> List[Dict]:
        """Analyze ATC check results from XML file."""
        issues = []
        
        try:
            tree = ET.parse(atc_xml_file)
            root = tree.getroot()
            
            # Parse ATC results XML structure
            for issue in root.findall(".//issue"):
                issue_data = {
                    "program": issue.find("program").text if issue.find("program") is not None else "",
                    "line": issue.find("line").text if issue.find("line") is not None else "",
                    "message": issue.find("message").text if issue.find("message") is not None else "",
                    "severity": issue.find("severity").text if issue.find("severity") is not None else "",
                    "type": issue.find("type").text if issue.find("type") is not None else ""
                }
                issues.append(issue_data)
                
        except Exception as e:
            self.logger.error(f"Error parsing ATC XML: {e}")
            
        return issues
        
    def detect_open_sql_issues(self, abap_code: str) -> List[Tuple[int, str, str]]:
        """Detect Open SQL syntax issues in ABAP code."""
        issues = []
        lines = abap_code.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            line = line.strip()
            
            # Check for Open SQL syntax patterns
            for pattern in self.config["fix_patterns"]["open_sql_syntax"]:
                if re.search(pattern, line, re.IGNORECASE):
                    issues.append((line_num, line, "open_sql_syntax"))
                    
            # Check for restricted language patterns
            for pattern in self.config["fix_patterns"]["restricted_language"]:
                if re.search(pattern, line, re.IGNORECASE):
                    issues.append((line_num, line, "restricted_language"))
                    
        return issues
        
    def fix_open_sql_syntax(self, abap_code: str) -> Tuple[str, List[str]]:
        """Fix Open SQL syntax issues in ABAP code."""
        fixed_code = abap_code
        fixes_applied = []
        lines = fixed_code.split('\n')
        
        for i, line in enumerate(lines):
            original_line = line
            
            # Fix Open SQL syntax issues
            for old_pattern, new_pattern in self.config["replacement_patterns"]["open_sql_syntax"].items():
                if old_pattern.lower() in line.lower():
                    line = re.sub(rf'\b{old_pattern}\b', new_pattern, line, flags=re.IGNORECASE)
                    if line != original_line:
                        fixes_applied.append(f"Line {i+1}: {old_pattern} -> {new_pattern}")
                        
            # Fix restricted language issues
            for old_pattern, new_pattern in self.config["replacement_patterns"]["restricted_language"].items():
                if old_pattern.lower() in line.lower():
                    line = re.sub(rf'\b{re.escape(old_pattern)}\b', new_pattern, line, flags=re.IGNORECASE)
                    if line != original_line:
                        fixes_applied.append(f"Line {i+1}: {old_pattern} -> {new_pattern}")
                        
            lines[i] = line
            
        return '\n'.join(lines), fixes_applied
        
    def process_abap_program(self, file_path: str) -> Dict:
        """Process a single ABAP program file."""
        result = {
            "file": file_path,
            "status": "success",
            "issues_found": 0,
            "fixes_applied": [],
            "backup_created": False,
            "error": None
        }
        
        try:
            # Read ABAP code
            with open(file_path, 'r', encoding='utf-8') as f:
                abap_code = f.read()
                
            # Create backup
            backup_path = self.create_backup(file_path)
            result["backup_created"] = backup_path != file_path
            result["backup_path"] = backup_path
            
            # Detect issues
            issues = self.detect_open_sql_issues(abap_code)
            result["issues_found"] = len(issues)
            
            if issues:
                # Apply fixes
                fixed_code, fixes = self.fix_open_sql_syntax(abap_code)
                result["fixes_applied"] = fixes
                
                # Write fixed code
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(fixed_code)
                    
                self.fixes_applied += len(fixes)
                self.errors_fixed += len(issues)
                
                self.logger.info(f"Fixed {len(fixes)} issues in {file_path}")
                
        except Exception as e:
            result["status"] = "error"
            result["error"] = str(e)
            self.logger.error(f"Error processing {file_path}: {e}")
            
        return result
        
    def process_directory(self, directory_path: str, file_pattern: str = "*.abap") -> List[Dict]:
        """Process all ABAP files in a directory."""
        results = []
        
        if not os.path.exists(directory_path):
            self.logger.error(f"Directory not found: {directory_path}")
            return results
            
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                if file.endswith('.abap') or file.endswith('.abap.txt'):
                    file_path = os.path.join(root, file)
                    result = self.process_abap_program(file_path)
                    results.append(result)
                    
        return results
        
    def generate_report(self, results: List[Dict], output_file: str = "atc_automation_report.html"):
        """Generate HTML report of the automation results."""
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>SAP ABAP ATC Automation Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .header {{ background-color: #f0f0f0; padding: 20px; border-radius: 5px; }}
        .summary {{ background-color: #e8f5e8; padding: 15px; border-radius: 5px; margin: 20px 0; }}
        .file-result {{ border: 1px solid #ddd; margin: 10px 0; padding: 15px; border-radius: 5px; }}
        .success {{ border-left: 5px solid #4CAF50; }}
        .error {{ border-left: 5px solid #f44336; }}
        .fixes {{ background-color: #fff3cd; padding: 10px; border-radius: 3px; margin: 10px 0; }}
        .timestamp {{ color: #666; font-size: 12px; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>SAP ABAP ATC Automation Report</h1>
        <p class="timestamp">Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>
    
    <div class="summary">
        <h2>Summary</h2>
        <p><strong>Total files processed:</strong> {len(results)}</p>
        <p><strong>Successful fixes:</strong> {self.fixes_applied}</p>
        <p><strong>Errors resolved:</strong> {self.errors_fixed}</p>
    </div>
    
    <h2>File Results</h2>
"""
        
        for result in results:
            status_class = "success" if result["status"] == "success" else "error"
            html_content += f"""
    <div class="file-result {status_class}">
        <h3>{result['file']}</h3>
        <p><strong>Status:</strong> {result['status']}</p>
        <p><strong>Issues found:</strong> {result['issues_found']}</p>
        <p><strong>Backup created:</strong> {result['backup_created']}</p>
"""
            
            if result["fixes_applied"]:
                html_content += f"""
        <div class="fixes">
            <strong>Fixes applied:</strong>
            <ul>
"""
                for fix in result["fixes_applied"]:
                    html_content += f"                <li>{fix}</li>\n"
                html_content += "            </ul>\n        </div>\n"
                
            if result["error"]:
                html_content += f"        <p><strong>Error:</strong> {result['error']}</p>\n"
                
            html_content += "    </div>\n"
            
        html_content += """
</body>
</html>
"""
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            self.logger.info(f"Report generated: {output_file}")
        except Exception as e:
            self.logger.error(f"Error generating report: {e}")
            
    def run_automation(self, target_path: str, is_directory: bool = True):
        """Run the complete automation process."""
        self.logger.info("Starting SAP ABAP ATC automation...")
        
        if is_directory:
            results = self.process_directory(target_path)
        else:
            results = [self.process_abap_program(target_path)]
            
        # Generate report
        self.generate_report(results)
        
        self.logger.info(f"Automation completed. Processed {len(results)} files.")
        self.logger.info(f"Total fixes applied: {self.fixes_applied}")
        self.logger.info(f"Total errors resolved: {self.errors_fixed}")
        
        return results

def main():
    """Main function to run the automation."""
    import argparse
    
    parser = argparse.ArgumentParser(description="SAP ABAP ATC Check Automation Tool")
    parser.add_argument("target", help="Target file or directory path")
    parser.add_argument("--file", action="store_true", help="Treat target as a single file")
    parser.add_argument("--config", default="atc_config.json", help="Configuration file path")
    
    args = parser.parse_args()
    
    # Initialize automation tool
    automation = SAPABAPATCAutomation(args.config)
    
    # Run automation
    results = automation.run_automation(args.target, not args.file)
    
    # Print summary
    print(f"\nAutomation Summary:")
    print(f"Files processed: {len(results)}")
    print(f"Fixes applied: {automation.fixes_applied}")
    print(f"Errors resolved: {automation.errors_fixed}")
    print(f"Report generated: atc_automation_report.html")

if __name__ == "__main__":
    main()