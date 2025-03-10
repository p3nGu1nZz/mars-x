"""
Build configuration settings for the Mars-X project.
"""

import os
from .base_config import BaseConfig

class BuildConfig(BaseConfig):
    """Configuration for build settings."""
    
    def __init__(self):
        """Initialize build configuration."""
        super().__init__("build")
        self._create_default_config()
        
    def _create_default_config(self):
        """Create default build configuration settings."""
        # Compiler settings
        self.set("compiler", "optimization_level", "O2")
        self.set("compiler", "debug_symbols", "False")
        self.set("compiler", "additional_flags", "/favor:AMD64 /DWIN64" if os.name == 'nt' else "-march=native")
        self.set("compiler", "parallel_jobs", "4")
        
        # Packager settings
        self.set("packager", "include_debug_files", "False")
        self.set("packager", "create_installer", "True")
        self.set("packager", "compression_level", "9")
        self.set("packager", "onefile", "True")
        
        # Asset settings
        self.set("assets", "compress_textures", "True")
        self.set("assets", "audio_quality", "medium")
        self.set("assets", "bundle_assets", "True")
        
        # Version settings
        self.set("version", "major", "0")
        self.set("version", "minor", "1")
        self.set("version", "patch", "0")
        self.set("version", "release_type", "alpha")
    
    def get_compiler_flags(self):
        """Get compiler flags for current platform."""
        flags = []
        
        # Add optimization level
        opt_level = self.get("compiler", "optimization_level", "O2")
        if os.name == 'nt':  # Windows
            if opt_level == "O0":
                flags.append("/Od")
            elif opt_level == "O1":
                flags.append("/O1")
            elif opt_level == "O3":
                flags.append("/Ox")
            else:  # Default to O2
                flags.append("/O2")
                
            # Add debug symbols if enabled
            if self.getboolean("compiler", "debug_symbols", False):
                flags.append("/Zi")
        else:  # Unix-like
            flags.append(f"-{opt_level}")
            
            # Add debug symbols if enabled
            if self.getboolean("compiler", "debug_symbols", False):
                flags.append("-g")
        
        # Add additional user-defined flags
        additional = self.get("compiler", "additional_flags", "")
        if additional:
            flags.extend(additional.split())
        
        return flags
    
    def get_version_string(self):
        """Get the current version string."""
        major = self.getint("version", "major", 0)
        minor = self.getint("version", "minor", 1)
        patch = self.getint("version", "patch", 0)
        release = self.get("version", "release_type", "alpha")
        
        return f"{major}.{minor}.{patch}-{release}"
    
    def increment_patch_version(self):
        """Increment the patch version number."""
        current = self.getint("version", "patch", 0)
        self.set("version", "patch", str(current + 1))
