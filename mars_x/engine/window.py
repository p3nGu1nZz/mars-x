import sdl2
import sdl2.ext
import logging

class Window:
    def __init__(self, title, width, height):
        self.width = width
        self.height = height
        self.title = title.encode('utf-8')  # SDL2 expects bytes for strings
        self.is_fullscreen = False  # Track fullscreen state
        
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
            raise RuntimeError(f"Failed to create SDL window: {sdl2.SDL_GetError().decode()}")
        
        logging.info(f"Window created: {width}x{height}")
    
    def get_sdl_window(self):
        """Get the underlying SDL window handle."""
        return self.window
    
    def get_vulkan_instance_extensions(self):
        """Get required Vulkan instance extensions for this window."""
        # Get the required Vulkan instance extensions from SDL
        extension_count = sdl2.c_uint32(0)
        sdl2.SDL_Vulkan_GetInstanceExtensions(self.window, extension_count, None)
        
        # Allocate memory for the extension names
        extensions = (sdl2.c_char_p * extension_count.value)()
        sdl2.SDL_Vulkan_GetInstanceExtensions(self.window, extension_count, extensions)
        
        # Convert to a Python list
        return [extensions[i].decode() for i in range(extension_count.value)]
    
    def create_vulkan_surface(self, instance):
        """Create a Vulkan surface for this window."""
        # Create a Vulkan surface for this window
        surface = sdl2.vk.VkSurfaceKHR()
        if not sdl2.SDL_Vulkan_CreateSurface(self.window, instance, surface):
            raise RuntimeError(f"Failed to create Vulkan surface: {sdl2.SDL_GetError().decode()}")
        return surface
    
    def toggle_fullscreen(self):
        """Toggle between windowed and fullscreen modes."""
        self.is_fullscreen = not self.is_fullscreen
        flags = sdl2.SDL_WINDOW_FULLSCREEN_DESKTOP if self.is_fullscreen else 0
        sdl2.SDL_SetWindowFullscreen(self.window, flags)
        
        # Get updated window size after toggle
        w = sdl2.c_int()
        h = sdl2.c_int()
        sdl2.SDL_GetWindowSize(self.window, w, h)
        self.width = w.value
        self.height = h.value
        
        logging.info(f"Window {'fullscreen' if self.is_fullscreen else 'windowed'} mode: {self.width}x{self.height}")
        return self.is_fullscreen
    
    def get_size(self):
        """Get the current window size."""
        w = sdl2.c_int()
        h = sdl2.c_int()
        sdl2.SDL_GetWindowSize(self.window, w, h)
        return (w.value, h.value)
    
    def cleanup(self):
        """Clean up resources."""
        if self.window:
            sdl2.SDL_DestroyWindow(self.window)
            self.window = None
            logging.info("Window destroyed")
