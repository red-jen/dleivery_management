#!/usr/bin/env python
"""
Test execution script - Run all project tests with detailed reporting.
"""
import subprocess
import sys
from pathlib import Path

def run_tests():
    """Run all tests and display results."""
    
    print("=" * 80)
    print("YouExpress Delivery API - Test Suite")
    print("=" * 80)
    print()
    
    # Get project root
    project_root = Path(__file__).parent
    
    # Run pytest with verbose output
    cmd = [
        sys.executable, "-m", "pytest",
        "tests/",
        "-v",
        "--tb=short",
        "--color=yes"
    ]
    
    print(f"Running: {' '.join(cmd)}")
    print()
    
    result = subprocess.run(cmd, cwd=project_root)
    
    print()
    print("=" * 80)
    
    if result.returncode == 0:
        print("✅ All tests passed!")
    else:
        print("⚠️  Some tests failed. See details above.")
    
    print("=" * 80)
    print()
    
    return result.returncode

if __name__ == "__main__":
    sys.exit(run_tests())
