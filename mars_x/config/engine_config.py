"""
Engine configuration settings for the Mars-X game.
"""

import os
from .base_config import BaseConfig

class EngineConfig(BaseConfig):
    """Configuration for the game engine."""
    
    def __init__(self):
        """Initialize engine configuration."""
        super().__init__("engine")
        self._create_default_config()
        
    def _create_default_config(self):
        """Create default configuration settings."""
        # Graphics settings
        self.set("graphics", "resolution_width", "1280")
        self.set("graphics", "resolution_height", "720")
        self.set("graphics", "fullscreen", "False")
        self.set("graphics", "vsync", "True")
        self.set("graphics", "max_fps", "60")
        
        # Audio settings
        self.set("audio", "master_volume", "0.8")
        self.set("audio", "music_volume", "0.7")
        self.set("audio", "sfx_volume", "1.0")
        self.set("audio", "mute", "False")
        
        # Input settings
        self.set("input", "mouse_sensitivity", "1.0")
        self.set("input", "invert_y", "False")
        self.set("input", "controller_enabled", "True")
        
        # Physics settings
        self.set("physics", "timestep", "0.016")  # 60 fps
        self.set("physics", "gravity", "9.81")
        self.set("physics", "simulation_quality", "medium")
        
        # Debug settings
        self.set("debug", "logging_level", "info")
        self.set("debug", "show_fps", "False")
        self.set("debug", "show_debug_info", "False")
    
    def get_resolution(self):
        """Get the current resolution as a tuple."""
        width = self.getint("graphics", "resolution_width", 1280)
        height = self.getint("graphics", "resolution_height", 720)
        return (width, height)
    
    def set_resolution(self, width, height):
        """Set the resolution."""
        self.set("graphics", "resolution_width", str(width))
        self.set("graphics", "resolution_height", str(height))
    
    def is_fullscreen(self):
        """Check if fullscreen is enabled."""
        return self.getboolean("graphics", "fullscreen", False)
    
    def set_fullscreen(self, enabled):
        """Set fullscreen mode."""
        self.set("graphics", "fullscreen", str(enabled))
    
    def get_master_volume(self):
        """Get master volume level."""
        return self.getfloat("audio", "master_volume", 0.8)
    
    def set_master_volume(self, volume):
        """Set master volume level."""
        self.set("audio", "master_volume", str(max(0.0, min(1.0, volume))))
