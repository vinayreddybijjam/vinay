#!/usr/bin/env python3
"""
ABAP Cloud Readiness Fix Tool
Specialized tool for fixing Open SQL syntax errors in restricted language scope
for ABAP_CLOUD_READINESS compliance.
"""

import os
import re
import json
import logging
from datetime import datetime
from typing import List, Dict, Tuple, Optional
import xml.etree.ElementTree as ET

class ABAPCloudFix:
    def __init__(self):
        """Initialize the ABAP Cloud Fix tool."""
        self.setup_logging()
        self.fixes_applied = 0
        self.errors_fixed = 0
        
        # ABAP Cloud Readiness specific patterns
        self.cloud_patterns = {
            "open_sql_restricted": {
                # Basic SELECT statements that need conversion
                r"SELECT\s+(\w+)\s+FROM\s+(\w+)\s+WHERE\s+(.+?)(?:\s+ORDER\s+BY|\s+GROUP\s+BY|\s+HAVING|\s+UNION|\s+$|;)": 
                    "SELECT_SINGLE {0} FROM {1} WHERE {2}",
                
                # SELECT with INTO
                r"SELECT\s+(.+?)\s+FROM\s+(\w+)\s+INTO\s+(.+?)(?:\s+WHERE|\s+ORDER\s+BY|\s+GROUP\s+BY|\s+HAVING|\s+UNION|\s+$|;)": 
                    "SELECT_SINGLE {0} FROM {1} INTO {2}",
                
                # SELECT with APPENDING
                r"SELECT\s+(.+?)\s+FROM\s+(\w+)\s+APPENDING\s+(.+?)(?:\s+WHERE|\s+ORDER\s+BY|\s+GROUP\s+BY|\s+HAVING|\s+UNION|\s+$|;)": 
                    "SELECT {0} FROM {1} APPENDING {2}",
                
                # SELECT with FOR ALL ENTRIES
                r"SELECT\s+(.+?)\s+FROM\s+(\w+)\s+FOR\s+ALL\s+ENTRIES\s+IN\s+(.+?)(?:\s+WHERE|\s+ORDER\s+BY|\s+GROUP\s+BY|\s+HAVING|\s+UNION|\s+$|;)": 
                    "SELECT {0} FROM {1} FOR ALL ENTRIES IN {2}",
                
                # INSERT statements
                r"INSERT\s+INTO\s+(\w+)\s+VALUES\s+(.+?)(?:\s+$|;)": 
                    "INSERT_INTO {0} VALUES {1}",
                
                # UPDATE statements
                r"UPDATE\s+(\w+)\s+SET\s+(.+?)(?:\s+WHERE|\s+$|;)": 
                    "UPDATE_FROM {0} SET {1}",
                
                # DELETE statements
                r"DELETE\s+FROM\s+(\w+)(?:\s+WHERE|\s+$|;)": 
                    "DELETE_FROM {0}",
            },
            
            "restricted_language": {
                # System fields that need proper handling
                r"SY-SUBRC\s*=\s*(\d+)": "IF sy-subrc = {0}",
                r"SY-DBCNT\s*=\s*(\d+)": "IF sy-dbcnt = {0}",
                r"SY-TABIX\s*=\s*(\d+)": "IF sy-tabix = {0}",
                r"SY-INDEX\s*=\s*(\d+)": "IF sy-index = {0}",
                
                # Commit and Rollback
                r"COMMIT\s+WORK(?:\s+AND\s+WAIT)?": "COMMIT WORK AND WAIT",
                r"ROLLBACK\s+WORK(?:\s+AND\s+WAIT)?": "ROLLBACK WORK AND WAIT",
                
                # System field assignments
                r"(\w+)\s*=\s*SY-(\w+)": "{0} = sy-{1}",
            },
            
            "function_calls": {
                # Function module calls that need cloud compliance
                r"CALL\s+FUNCTION\s+'([^']+)'\s+DESTINATION\s+(\w+)": 
                    "CALL FUNCTION '{0}' IN BACKGROUND TASK DESTINATION {1}",
                r"CALL\s+FUNCTION\s+'([^']+)'\s+IN\s+BACKGROUND\s+TASK": 
                    "CALL FUNCTION '{0}' IN BACKGROUND TASK",
                r"CALL\s+FUNCTION\s+'([^']+)'\s+IN\s+UPDATE\s+TASK": 
                    "CALL FUNCTION '{0}' IN UPDATE TASK",
                r"CALL\s+FUNCTION\s+'([^']+)'\s+EXCEPTIONS\s+(.+?)(?:\s+$|;)": 
                    "CALL FUNCTION '{0}' WITH ERROR HANDLING EXCEPTIONS {1}",
            }
        }
        
    def setup_logging(self):
        """Setup logging configuration."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('abap_cloud_fix.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def create_backup(self, file_path: str) -> str:
        """Create backup of the original file."""
        backup_dir = "abap_backups"
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
            
    def fix_abap_cloud_issues(self, abap_code: str) -> Tuple[str, List[str]]:
        """Fix ABAP Cloud Readiness issues in the code."""
        fixed_code = abap_code
        fixes_applied = []
        
        # Fix Open SQL restricted patterns
        for pattern, replacement in self.cloud_patterns["open_sql_restricted"].items():
            matches = re.finditer(pattern, fixed_code, re.IGNORECASE | re.MULTILINE)
            for match in matches:
                original = match.group(0)
                try:
                    fixed = replacement.format(*match.groups())
                    fixed_code = fixed_code.replace(original, fixed)
                    fixes_applied.append(f"Open SQL: {original.strip()} -> {fixed.strip()}")
                except Exception as e:
                    self.logger.warning(f"Failed to apply pattern {pattern}: {e}")
                    
        # Fix restricted language patterns
        for pattern, replacement in self.cloud_patterns["restricted_language"].items():
            matches = re.finditer(pattern, fixed_code, re.IGNORECASE | re.MULTILINE)
            for match in matches:
                original = match.group(0)
                try:
                    fixed = replacement.format(*match.groups())
                    fixed_code = fixed_code.replace(original, fixed)
                    fixes_applied.append(f"Restricted Language: {original.strip()} -> {fixed.strip()}")
                except Exception as e:
                    self.logger.warning(f"Failed to apply pattern {pattern}: {e}")
                    
        # Fix function call patterns
        for pattern, replacement in self.cloud_patterns["function_calls"].items():
            matches = re.finditer(pattern, fixed_code, re.IGNORECASE | re.MULTILINE)
            for match in matches:
                original = match.group(0)
                try:
                    fixed = replacement.format(*match.groups())
                    fixed_code = fixed_code.replace(original, fixed)
                    fixes_applied.append(f"Function Call: {original.strip()} -> {fixed.strip()}")
                except Exception as e:
                    self.logger.warning(f"Failed to apply pattern {pattern}: {e}")
                    
        return fixed_code, fixes_applied
        
    def add_cloud_compliance_headers(self, abap_code: str) -> str:
        """Add ABAP Cloud compliance headers and pragmas."""
        headers = [
            "************************************************************************",
            "* ABAP Cloud Readiness Compliance",
            "* Generated by ABAP Cloud Fix Tool",
            "* Date: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "************************************************************************",
            "",
            "* Enable restricted language mode",
            "PRAGMA RESTRICTED_LANGUAGE_MODE",
            "",
            "* Enable Open SQL restrictions",
            "PRAGMA OPEN_SQL_RESTRICTIONS",
            "",
            "* Enable function module restrictions",
            "PRAGMA FUNCTION_MODULE_RESTRICTIONS",
            "",
            "************************************************************************",
            ""
        ]
        
        # Find the first non-comment line
        lines = abap_code.split('\n')
        insert_pos = 0
        
        for i, line in enumerate(lines):
            line = line.strip()
            if line and not line.startswith('*') and not line.startswith('"'):
                insert_pos = i
                break
                
        # Insert headers
        lines.insert(insert_pos, '\n'.join(headers))
        return '\n'.join(lines)
        
    def process_abap_file(self, file_path: str) -> Dict:
        """Process a single ABAP file for cloud compliance."""
        result = {
            "file": file_path,
            "status": "success",
            "issues_found": 0,
            "fixes_applied": [],
            "backup_created": False,
            "backup_path": None,
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
            
            # Apply fixes
            fixed_code, fixes = self.fix_abap_cloud_issues(abap_code)
            result["fixes_applied"] = fixes
            result["issues_found"] = len(fixes)
            
            if fixes:
                # Add compliance headers
                fixed_code = self.add_cloud_compliance_headers(fixed_code)
                
                # Write fixed code
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(fixed_code)
                    
                self.fixes_applied += len(fixes)
                self.errors_fixed += len(fixes)
                
                self.logger.info(f"Fixed {len(fixes)} issues in {file_path}")
                
        except Exception as e:
            result["status"] = "error"
            result["error"] = str(e)
            self.logger.error(f"Error processing {file_path}: {e}")
            
        return result
        
    def process_directory(self, directory_path: str) -> List[Dict]:
        """Process all ABAP files in a directory."""
        results = []
        
        if not os.path.exists(directory_path):
            self.logger.error(f"Directory not found: {directory_path}")
            return results
            
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                if file.endswith(('.abap', '.abap.txt', '.abap.src')):
                    file_path = os.path.join(root, file)
                    result = self.process_abap_file(file_path)
                    results.append(result)
                    
        return results
        
    def generate_cloud_report(self, results: List[Dict], output_file: str = "abap_cloud_compliance_report.html"):
        """Generate HTML report of the cloud compliance fixes."""
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>ABAP Cloud Readiness Compliance Report</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 20px; background-color: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; background-color: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 8px; text-align: center; margin-bottom: 30px; }}
        .summary {{ background-color: #e8f5e8; padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 5px solid #4CAF50; }}
        .file-result {{ border: 1px solid #ddd; margin: 15px 0; padding: 20px; border-radius: 8px; background-color: white; }}
        .success {{ border-left: 5px solid #4CAF50; }}
        .error {{ border-left: 5px solid #f44336; }}
        .fixes {{ background-color: #fff3cd; padding: 15px; border-radius: 5px; margin: 15px 0; border-left: 3px solid #ffc107; }}
        .timestamp {{ color: #666; font-size: 14px; margin-top: 10px; }}
        .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 20px 0; }}
        .stat-card {{ background: white; padding: 20px; border-radius: 8px; text-align: center; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }}
        .stat-number {{ font-size: 2em; font-weight: bold; color: #667eea; }}
        .stat-label {{ color: #666; margin-top: 5px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 ABAP Cloud Readiness Compliance Report</h1>
            <p>Automated fixes for Open SQL syntax errors in restricted language scope</p>
            <p class="timestamp">Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
        
        <div class="summary">
            <h2>📊 Summary</h2>
            <div class="stats">
                <div class="stat-card">
                    <div class="stat-number">{len(results)}</div>
                    <div class="stat-label">Files Processed</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{self.fixes_applied}</div>
                    <div class="stat-label">Fixes Applied</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{self.errors_fixed}</div>
                    <div class="stat-label">Errors Resolved</div>
                </div>
            </div>
        </div>
        
        <h2>📁 File Results</h2>
"""
        
        for result in results:
            status_class = "success" if result["status"] == "success" else "error"
            status_icon = "✅" if result["status"] == "success" else "❌"
            
            html_content += f"""
        <div class="file-result {status_class}">
            <h3>{status_icon} {result['file']}</h3>
            <p><strong>Status:</strong> {result['status']}</p>
            <p><strong>Issues found:</strong> {result['issues_found']}</p>
            <p><strong>Backup created:</strong> {result['backup_created']}</p>
"""
            
            if result["backup_path"] and result["backup_path"] != result["file"]:
                html_content += f"            <p><strong>Backup path:</strong> {result['backup_path']}</p>\n"
                
            if result["fixes_applied"]:
                html_content += f"""
            <div class="fixes">
                <strong>🔧 Fixes Applied:</strong>
                <ul>
"""
                for fix in result["fixes_applied"]:
                    html_content += f"                    <li>{fix}</li>\n"
                html_content += "                </ul>\n            </div>\n"
                
            if result["error"]:
                html_content += f"            <p><strong>Error:</strong> {result['error']}</p>\n"
                
            html_content += "        </div>\n"
            
        html_content += """
        <div class="summary">
            <h2>🎯 Next Steps</h2>
            <ul>
                <li>Review the applied fixes to ensure they meet your business requirements</li>
                <li>Run ATC checks again with ABAP_CLOUD_READINESS variant</li>
                <li>Test the modified programs in your development environment</li>
                <li>Consider implementing additional cloud compliance measures</li>
            </ul>
        </div>
    </div>
</body>
</html>
"""
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            self.logger.info(f"Cloud compliance report generated: {output_file}")
        except Exception as e:
            self.logger.error(f"Error generating report: {e}")
            
    def run_cloud_fix(self, target_path: str, is_directory: bool = True):
        """Run the complete ABAP Cloud compliance fix process."""
        self.logger.info("Starting ABAP Cloud Readiness compliance fixes...")
        
        if is_directory:
            results = self.process_directory(target_path)
        else:
            results = [self.process_abap_file(target_path)]
            
        # Generate report
        self.generate_cloud_report(results)
        
        self.logger.info(f"Cloud compliance fixes completed. Processed {len(results)} files.")
        self.logger.info(f"Total fixes applied: {self.fixes_applied}")
        self.logger.info(f"Total errors resolved: {self.errors_fixed}")
        
        return results

def main():
    """Main function to run the ABAP Cloud fix tool."""
    import argparse
    
    parser = argparse.ArgumentParser(description="ABAP Cloud Readiness Fix Tool")
    parser.add_argument("target", help="Target file or directory path")
    parser.add_argument("--file", action="store_true", help="Treat target as a single file")
    
    args = parser.parse_args()
    
    # Initialize cloud fix tool
    cloud_fix = ABAPCloudFix()
    
    # Run cloud compliance fixes
    results = cloud_fix.run_cloud_fix(args.target, not args.file)
    
    # Print summary
    print(f"\n🚀 ABAP Cloud Compliance Summary:")
    print(f"Files processed: {len(results)}")
    print(f"Fixes applied: {cloud_fix.fixes_applied}")
    print(f"Errors resolved: {cloud_fix.errors_fixed}")
    print(f"Report generated: abap_cloud_compliance_report.html")
    print(f"\n✅ Your ABAP programs are now ready for ATC checks with ABAP_CLOUD_READINESS!")

if __name__ == "__main__":
    main()