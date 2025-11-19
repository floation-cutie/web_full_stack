"""
Comprehensive API Test Runner for GoodServices Platform

This script runs all comprehensive tests and generates a detailed report.
"""

import subprocess
import sys
import json
from datetime import datetime


def run_tests():
    """Run pytest with comprehensive reporting"""
    print("=" * 80)
    print("GoodServices Platform - Comprehensive API Testing")
    print("=" * 80)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    print()

    # Run pytest with verbose output and JSON report
    cmd = [
        "pytest",
        "tests/test_comprehensive_api.py",
        "-v",
        "--tb=short",
        "--color=yes",
        "-s"
    ]

    try:
        result = subprocess.run(
            cmd,
            cwd="/home/cutie/Agent-Helper/web_full_stack/backend",
            capture_output=False,
            text=True
        )

        print()
        print("=" * 80)
        print(f"Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 80)

        return result.returncode

    except Exception as e:
        print(f"Error running tests: {e}")
        return 1


if __name__ == "__main__":
    exit_code = run_tests()
    sys.exit(exit_code)
