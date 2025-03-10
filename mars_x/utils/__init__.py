"""
Mars-X Utilities Package.

This package contains various utility modules and helper functions used
throughout the Mars-X project, including constants, setup helpers, and
other common functionality.
"""

from .constants import (
    PROJECT_ROOT, 
    VENV_DIR, 
    SOURCE_DIR, 
    RESOURCES_DIR, 
    BUILD_DIR,
    GAME_NAME,
    GAME_VERSION,
    GAME_AUTHOR,
    GAME_DESCRIPTION
)

from .setup_help import print_help

# Import version information
__version__ = GAME_VERSION
