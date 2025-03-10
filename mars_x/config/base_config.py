"""
Base configuration class that other configuration classes inherit from.
"""

import os
import configparser
import shutil
from . import USER_CONFIG_DIR, CONFIG_FILES_DIR

class BaseConfig:
    """Base class for all configuration objects."""
    
    def __init__(self, config_name="config"):
        """Initialize configuration with specified name."""
        self.config_name = config_name
        self.config = configparser.ConfigParser(comment_prefixes=('#', ';'))
        
        # Define file paths - look in multiple locations
        self.default_path = os.path.join(CONFIG_FILES_DIR, f"{config_name}.ini")
        self.user_path = os.path.join(USER_CONFIG_DIR, f"{config_name}.ini")
        
        # For development/testing, also check local directory
        self.local_path = os.path.abspath(f"{config_name}.ini")
        
    def load(self):
        """Load configuration from default and user files."""
        loaded = False
        
        # First load defaults if they exist
        if os.path.exists(self.default_path):
            self.config.read(self.default_path)
            loaded = True
            print(f"Loaded default config from {self.default_path}")
        
        # Then check for local config file (useful during development)
        if os.path.exists(self.local_path):
            self.config.read(self.local_path)
            loaded = True
            print(f"Loaded local config from {self.local_path}")
            
        # Finally load user config, which has highest priority
        if os.path.exists(self.user_path):
            self.config.read(self.user_path)
            loaded = True
            print(f"Loaded user config from {self.user_path}")
        
        if not loaded:
            print(f"No configuration files found for {self.config_name}. Creating defaults...")
            self._create_default_config()
            self.save()
            
        return loaded
    
    def save(self):
        """Save current configuration to user file."""
        os.makedirs(os.path.dirname(self.user_path), exist_ok=True)
        
        with open(self.user_path, 'w') as f:
            self.config.write(f)
            
        return True
    
    def _create_default_config(self):
        """Create default configuration - to be overridden by subclasses."""
        pass
    
    def get(self, section, option, fallback=None):
        """Get a configuration value."""
        return self.config.get(section, option, fallback=fallback)
    
    def getint(self, section, option, fallback=None):
        """Get an integer configuration value."""
        return self.config.getint(section, option, fallback=fallback)
    
    def getfloat(self, section, option, fallback=None):
        """Get a float configuration value."""
        return self.config.getfloat(section, option, fallback=fallback)
    
    def getboolean(self, section, option, fallback=None):
        """Get a boolean configuration value."""
        return self.config.getboolean(section, option, fallback=fallback)
    
    def set(self, section, option, value):
        """Set a configuration value."""
        if not self.config.has_section(section):
            self.config.add_section(section)
        
        self.config.set(section, option, str(value))
        return True
