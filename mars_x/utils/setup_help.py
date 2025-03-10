"""
Helper functions for displaying setup information and usage instructions.
"""

import os
import sys


def print_help():
    """Display help information in standard CLI format."""
    program_name = os.path.basename(sys.argv[0])
    
    print(f"""
Usage: python {program_name} [OPTIONS] [COMMAND]

Mars-X Game Engine setup utility

Commands:
  --build                Build Cython modules and executable
  --help                 Show this help message and exit

Options:
  --update              Update existing virtual environment and dependencies

Examples:
  python {program_name}                    Set up development environment
  python {program_name} --build            Build Cython modules and executable
  python {program_name} --update           Update existing environment and dependencies
  
For more information, visit: https://github.com/p3nGu1nZz/mars-x
""")
