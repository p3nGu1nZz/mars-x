"""
Configuration system for Mars-X game engine.
This module provides tools to read, write and manage game configuration settings.
"""

import os
import configparser
import shutil
import sys
from pathlib import Path

# Try to import appdirs, but provide a fallback
try:
    import appdirs
    USER_CONFIG_DIR = appdirs.user_config_dir("mars-x")
except ImportError:
    print("ERROR: Required package 'appdirs' is not installed.")
    print("Please install it with: pip install appdirs")
    sys.exit(1)

# Define standard configuration directories
CONFIG_FILES_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config_files")

# Check if config directory path is overridden (e.g., by packaged app)
if "MARS_X_CONFIG_DIR" in os.environ:
    CONFIG_FILES_DIR = os.environ["MARS_X_CONFIG_DIR"]
    print(f"Using configuration directory from environment: {CONFIG_FILES_DIR}")

# Ensure directories exist
os.makedirs(CONFIG_FILES_DIR, exist_ok=True)
os.makedirs(USER_CONFIG_DIR, exist_ok=True)

# Create path to user configuration
USER_CONFIG = os.path.join(USER_CONFIG_DIR, "config.ini")

# Import configs (deferred to avoid circular imports)
def _import_configs():
    global engine_config, build_config
    from .engine_config import EngineConfig
    from .build_config import BuildConfig
    
    # Global configuration instances
    engine_config = EngineConfig()
    build_config = BuildConfig()
    return engine_config, build_config

# Placeholder config instances that will be initialized later
engine_config = None
build_config = None

def initialize():
    """
    Initialize all configuration systems.
    Loads default and user configurations.
    """
    # Import configs if needed
    global engine_config, build_config
    if engine_config is None or build_config is None:
        engine_config, build_config = _import_configs()
    
    # Copy default configuration files to user directory if they don't exist
    _ensure_config_files_exist()
    
    # Load configurations
    engine_config.load()
    build_config.load()
    
    print(f"Configuration loaded from {USER_CONFIG_DIR}")
    return True

def save_all():
    """Save all configuration to disk."""
    # Import configs if needed
    global engine_config, build_config
    if engine_config is None or build_config is None:
        engine_config, build_config = _import_configs()
    
    engine_config.save()
    build_config.save()
    
    print(f"Configuration saved to {USER_CONFIG_DIR}")
    return True

def _ensure_config_files_exist():
    """Ensure all configuration files exist in the user directory."""
    for config_file in ['engine.ini', 'build.ini']:
        source = os.path.join(CONFIG_FILES_DIR, config_file)
        destination = os.path.join(USER_CONFIG_DIR, config_file)
        
        # If the source file exists but destination doesn't, copy it
        if os.path.exists(source) and not os.path.exists(destination):
            shutil.copy2(source, destination)
            print(f"Created default config file: {destination}")

# Actually load the configs on the first import
_import_configs()
