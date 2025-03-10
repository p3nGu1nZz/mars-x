import sdl2
import sdl2.ext

class Window:
    def __init__(self, title, width, height):
        self.width = width
        self.height = height
        self.title = title.encode('utf-8')  # SDL2 expects bytes for strings
        
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
    
    def get_sdl_window(self):
        return self.window
    
    def get_vulkan_instance_extensions(self):
        # Get the required Vulkan instance extensions from SDL
        extension_count = sdl2.c_uint32(0)
        sdl2.SDL_Vulkan_GetInstanceExtensions(self.window, extension_count, None)
        
        # Allocate memory for the extension names
        extensions = (sdl2.c_char_p * extension_count.value)()
        sdl2.SDL_Vulkan_GetInstanceExtensions(self.window, extension_count, extensions)
        
        # Convert to a Python list
        return [extensions[i].decode() for i in range(extension_count.value)]
    
    def create_vulkan_surface(self, instance):
        # Create a Vulkan surface for this window
        surface = sdl2.vk.VkSurfaceKHR()
        if not sdl2.SDL_Vulkan_CreateSurface(self.window, instance, surface):
            raise RuntimeError(f"Failed to create Vulkan surface: {sdl2.SDL_GetError()}")
        return surface
    
    def cleanup(self):
        if self.window:
            sdl2.SDL_DestroyWindow(self.window)
            self.window = None
