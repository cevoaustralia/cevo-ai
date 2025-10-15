#!/usr/bin/env python3
import unittest
import sys
import os

def run_tests(test_type="all"):
    """Run specified test suite"""
    
    # Add backend to path
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))
    
    if test_type == "unit":
        suite = unittest.TestLoader().discover('backend/tests', pattern='test_unit.py')
    elif test_type == "functional":
        suite = unittest.TestLoader().discover('backend/tests', pattern='test_functional.py')
    elif test_type == "integration":
        suite = unittest.TestLoader().discover('backend/tests', pattern='test_integration.py')
    else:
        suite = unittest.TestLoader().discover('backend/tests', pattern='test_*.py')
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()

if __name__ == '__main__':
    test_type = sys.argv[1] if len(sys.argv) > 1 else "all"
    success = run_tests(test_type)
    sys.exit(0 if success else 1)