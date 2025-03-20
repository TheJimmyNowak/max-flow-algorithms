import pytest
import sys
from pathlib import Path

def run_tests():
    """Run all tests with coverage reporting."""
    # Get the project root directory
    project_root = Path(__file__).parent
    
    # Configure pytest arguments
    pytest_args = [
        'tests/',
        '--verbose',
        '--cov=src',
        '--cov-report=term-missing',
        '--cov-report=html',
        '--no-cov-on-fail',
        '--color=yes'
    ]
    
    # Run pytest
    exit_code = pytest.main(pytest_args)
    
    if exit_code == 0:
        print("\n✅ All tests passed successfully!")
        print(f"\nCoverage report generated in: {project_root}/htmlcov/index.html")
    else:
        print("\n❌ Some tests failed. Please check the output above for details.")
    
    return exit_code

if __name__ == '__main__':
    sys.exit(run_tests()) 