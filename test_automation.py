#!/usr/bin/env python3
"""
Test script to demonstrate the SAP ABAP ATC automation tools.
This script shows how the tools fix Open SQL syntax errors in restricted language scope.
"""

import os
import subprocess
import sys

def test_abap_cloud_fix():
    """Test the ABAP Cloud Fix tool with the example program."""
    print("🧪 Testing ABAP Cloud Fix Tool")
    print("=" * 50)
    
    # Check if example program exists
    if not os.path.exists("example_program.abap"):
        print("❌ Example program not found. Please ensure 'example_program.abap' exists.")
        return False
    
    # Check if the tool exists
    if not os.path.exists("abap_cloud_fix.py"):
        print("❌ ABAP Cloud Fix tool not found. Please ensure 'abap_cloud_fix.py' exists.")
        return False
    
    try:
        # Run the tool on the example program
        print("📝 Running ABAP Cloud Fix tool on example_program.abap...")
        result = subprocess.run([
            sys.executable, "abap_cloud_fix.py", "example_program.abap", "--file"
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ Tool executed successfully!")
            print("\n📊 Output:")
            print(result.stdout)
            
            # Check if backup was created
            if os.path.exists("abap_backups"):
                backup_files = os.listdir("abap_backups")
                if backup_files:
                    print(f"\n💾 Backup created: abap_backups/{backup_files[0]}")
            
            # Check if report was generated
            if os.path.exists("abap_cloud_compliance_report.html"):
                print("📄 Report generated: abap_cloud_compliance_report.html")
            
            # Show the fixed program
            print("\n🔍 Fixed program preview:")
            with open("example_program.abap", "r") as f:
                lines = f.readlines()
                for i, line in enumerate(lines[:20], 1):  # Show first 20 lines
                    print(f"{i:3d}: {line.rstrip()}")
                if len(lines) > 20:
                    print("     ... (truncated)")
            
            return True
        else:
            print("❌ Tool execution failed!")
            print("Error output:")
            print(result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Tool execution timed out!")
        return False
    except Exception as e:
        print(f"❌ Error testing tool: {e}")
        return False

def test_general_atc_tool():
    """Test the general ATC automation tool."""
    print("\n🧪 Testing General ATC Automation Tool")
    print("=" * 50)
    
    if not os.path.exists("sap_abap_atc_automation.py"):
        print("❌ General ATC tool not found. Please ensure 'sap_abap_atc_automation.py' exists.")
        return False
    
    try:
        # Run the tool on the current directory
        print("📝 Running General ATC tool on current directory...")
        result = subprocess.run([
            sys.executable, "sap_abap_atc_automation.py", "."
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ Tool executed successfully!")
            print("\n📊 Output:")
            print(result.stdout)
            
            # Check if report was generated
            if os.path.exists("atc_automation_report.html"):
                print("📄 Report generated: atc_automation_report.html")
            
            return True
        else:
            print("❌ Tool execution failed!")
            print("Error output:")
            print(result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Tool execution timed out!")
        return False
    except Exception as e:
        print(f"❌ Error testing tool: {e}")
        return False

def show_file_structure():
    """Show the current file structure."""
    print("\n📁 Current File Structure")
    print("=" * 50)
    
    files = [
        "sap_abap_atc_automation.py",
        "abap_cloud_fix.py", 
        "atc_config.json",
        "example_program.abap",
        "README.md"
    ]
    
    for file in files:
        if os.path.exists(file):
            size = os.path.getsize(file)
            print(f"✅ {file:<30} ({size:,} bytes)")
        else:
            print(f"❌ {file:<30} (missing)")
    
    # Check for generated files
    generated_files = [
        "abap_backups/",
        "backups/",
        "abap_cloud_compliance_report.html",
        "atc_automation_report.html"
    ]
    
    print("\n📊 Generated Files:")
    for file in generated_files:
        if os.path.exists(file):
            if os.path.isdir(file):
                items = len(os.listdir(file)) if os.path.exists(file) else 0
                print(f"📁 {file:<30} ({items} items)")
            else:
                size = os.path.getsize(file)
                print(f"📄 {file:<30} ({size:,} bytes)")
        else:
            print(f"⏳ {file:<30} (not yet generated)")

def main():
    """Main test function."""
    print("🚀 SAP ABAP ATC Automation Tools - Test Suite")
    print("=" * 60)
    
    # Show current file structure
    show_file_structure()
    
    # Test the tools
    success = True
    
    if not test_abap_cloud_fix():
        success = False
    
    if not test_general_atc_tool():
        success = False
    
    # Final summary
    print("\n" + "=" * 60)
    if success:
        print("🎉 All tests completed successfully!")
        print("\n📋 Next Steps:")
        print("1. Review the generated reports")
        print("2. Check the modified example_program.abap")
        print("3. Verify backups were created")
        print("4. Test with your own ABAP programs")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
    
    print("\n📚 For more information, see README.md")
    print("🔧 To use the tools, run:")
    print("   python3 abap_cloud_fix.py your_program.abap --file")
    print("   python3 sap_abap_atc_automation.py /path/to/programs/")

if __name__ == "__main__":
    main()