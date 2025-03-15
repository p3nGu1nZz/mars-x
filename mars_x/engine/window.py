import os
import sys
import sdl2
import sdl2.ext
import ctypes
import logging

# Load SDL2 library directly for Vulkan access
def _load_sdl2_vulkan_functions():
    """Load SDL2 Vulkan functions directly via ctypes as PySDL2 doesn't expose them properly."""
    try:
        # First, find the SDL2 library
        if hasattr(sdl2, 'SDL_GetBasePath'):
            # PySDL2 has already loaded the library
            if sys.platform == 'win32':
                sdl_lib = ctypes.WinDLL('SDL2.dll')
            else:
                sdl_lib = ctypes.CDLL('libSDL2-2.0.so.0')
                
            # Define function prototypes
            sdl_lib.SDL_Vulkan_GetInstanceExtensions.argtypes = [
                ctypes.c_void_p,  # SDL_Window*
                ctypes.POINTER(ctypes.c_uint32),  # uint32_t*
                ctypes.POINTER(ctypes.c_char_p)   # const char**
            ]
            sdl_lib.SDL_Vulkan_GetInstanceExtensions.restype = ctypes.c_bool
            
            sdl_lib.SDL_Vulkan_CreateSurface.argtypes = [
                ctypes.c_void_p,  # SDL_Window*
                ctypes.c_void_p,  # VkInstance
                ctypes.c_void_p   # VkSurfaceKHR*
            ]
            sdl_lib.SDL_Vulkan_CreateSurface.restype = ctypes.c_bool
            
            return sdl_lib
        else:
            logging.error("SDL2 library not properly initialized")
            return None
    except Exception as e:
        logging.error(f"Failed to load SDL2 Vulkan functions: {e}")
        return None

# Try to load SDL2 Vulkan functions
_sdl_lib_vulkan = _load_sdl2_vulkan_functions()

class Window:
    def __init__(self, title, width, height):
        self.width = width
        self.height = height
        self.title = title.encode('utf-8')  # SDL2 expects bytes for strings
        self.fullscreen = False
        
        # Create SDL window with Vulkan flag
        self.window = sdl2.SDL_CreateWindow(
            self.title,
            sdl2.SDL_WINDOWPOS_CENTERED, 
            sdl2.SDL_WINDOWPOS_CENTERED,
            self.width, 
            self.height,
            sdl2.SDL_WINDOW_VULKAN | sdl2.SDL_WINDOW_RESIZABLE
        )
        
        if not self.window:
            raise RuntimeError(f"Failed to create SDL window: {sdl2.SDL_GetError()}")
            
        # Check that we can access the Vulkan functions
        if not _sdl_lib_vulkan:
            # Fall back to software renderer for now
            logging.warning("Vulkan functions not available in SDL2, falling back to software renderer")
    
    def get_sdl_window(self):
        return self.window
    
    def get_vulkan_instance_extensions(self):
        """Get required Vulkan instance extensions for this window."""
        if not _sdl_lib_vulkan:
            logging.error("SDL2 Vulkan functions not available")
            return ["VK_KHR_surface", "VK_KHR_win32_surface"]  # Default extensions as fallback
        
        # Get the count of extensions
        extension_count = ctypes.c_uint32(0)
        success = _sdl_lib_vulkan.SDL_Vulkan_GetInstanceExtensions(
            self.window, 
            ctypes.byref(extension_count), 
            None
        )
        
        if not success:
            logging.error("Failed to get Vulkan instance extension count")
            return ["VK_KHR_surface", "VK_KHR_win32_surface"]  # Fallback
            
        # Get the extension names
        extensions_array = (ctypes.c_char_p * extension_count.value)()
        success = _sdl_lib_vulkan.SDL_Vulkan_GetInstanceExtensions(
            self.window,
            ctypes.byref(extension_count),
            extensions_array
        )
        
        if not success:
            logging.error("Failed to get Vulkan instance extensions")
            return ["VK_KHR_surface", "VK_KHR_win32_surface"]  # Fallback
            
        # Convert to Python strings
        extensions = [extensions_array[i].decode() for i in range(extension_count.value)]
        logging.info(f"Required Vulkan extensions: {extensions}")
        return extensions
    
    def create_vulkan_surface(self, instance):
        """Create a Vulkan surface for this window."""
        if not _sdl_lib_vulkan:
            logging.error("SDL2 Vulkan functions not available")
            return None
            
        # Create the surface
        surface = ctypes.c_void_p(0)  # VkSurfaceKHR is just a handle (uint64_t)
        success = _sdl_lib_vulkan.SDL_Vulkan_CreateSurface(
            self.window,
            instance,
            ctypes.byref(surface)
        )
        
        if not success:
            logging.error(f"Failed to create Vulkan surface: {sdl2.SDL_GetError()}")
            return None
            
        logging.info("Vulkan surface created successfully")
        return surface
    
    def toggle_fullscreen(self):
        """Toggle between windowed and fullscreen modes."""
        if not self.window:
            logging.error("Cannot toggle fullscreen: window is null")
            return False
            
        self.fullscreen = not self.fullscreen
        
        flag = sdl2.SDL_WINDOW_FULLSCREEN_DESKTOP if self.fullscreen else 0
        result = sdl2.SDL_SetWindowFullscreen(self.window, flag)
        
        if result == 0:
            mode = "fullscreen" if self.fullscreen else "windowed"
            logging.info(f"Window switched to {mode} mode")
            return True
        else:
            error = sdl2.SDL_GetError()
            logging.error(f"Failed to toggle fullscreen: {error}")
            # Reset our tracking variable to match reality
            self.fullscreen = not self.fullscreen
            return False
    
    def cleanup(self):
        if self.window:
            sdl2.SDL_DestroyWindow(self.window)
            self.window = None
