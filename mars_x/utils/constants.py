"""
Constants used throughout the Mars-X project.
"""

from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
VENV_DIR = PROJECT_ROOT / ".venv"
SOURCE_DIR = PROJECT_ROOT / "mars_x"
RESOURCES_DIR = PROJECT_ROOT / "resources"
BUILD_DIR = PROJECT_ROOT / "build"

# Game settings
GAME_NAME = "Mars-X"
GAME_VERSION = "0.1.0"
GAME_AUTHOR = "3nigma"
GAME_DESCRIPTION = "A 2D top-down space flight game"

# Default configuration
DEFAULT_SCREEN_WIDTH = 1280
DEFAULT_SCREEN_HEIGHT = 720
DEFAULT_FULLSCREEN = False
DEFAULT_VSYNC = True
