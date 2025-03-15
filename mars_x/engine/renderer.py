import vulkan as vk
import logging
import sdl2
from mars_x.engine.window import Window

class VulkanRenderer:
    def __init__(self, window):
        self.window = window
        self.instance = None
        self.device = None
        self.surface = None
        self.swap_chain = None
        
        # Add SDL renderer for fallback/simple rendering
        self.sdl_renderer = None
        
        try:
            self._initialize_vulkan()
        except Exception as e:
            logging.error(f"Failed to initialize Vulkan: {e}")
            self._initialize_fallback()
    
    def _initialize_fallback(self):
        """Initialize a fallback SDL2 renderer when Vulkan isn't available."""
        logging.warning("Using SDL2 fallback renderer")
        
        # Create an SDL2 renderer
        self.sdl_renderer = sdl2.SDL_CreateRenderer(
            self.window.get_sdl_window(),
            -1,
            sdl2.SDL_RENDERER_ACCELERATED | sdl2.SDL_RENDERER_PRESENTVSYNC
        )
        
        if not self.sdl_renderer:
            error = sdl2.SDL_GetError()
            logging.error(f"Failed to create SDL renderer: {error}")
            raise RuntimeError("Failed to create SDL renderer")
            
        logging.info("SDL2 fallback renderer initialized")
    
    def _initialize_vulkan(self):
        # Create Vulkan instance
        app_info = vk.VkApplicationInfo(
            pApplicationName="Mars-X",
            applicationVersion=vk.VK_MAKE_VERSION(1, 0, 0),
            pEngineName="Mars-X Engine",
            engineVersion=vk.VK_MAKE_VERSION(1, 0, 0),
            apiVersion=vk.VK_API_VERSION_1_0
        )
        
        # Get required extensions
        try:
            extensions = self.window.get_vulkan_instance_extensions()
            logging.info(f"Using Vulkan extensions: {extensions}")
            
            # Add debug extension if needed
            if vk.VK_EXT_DEBUG_UTILS_EXTENSION_NAME not in extensions:
                extensions.append(vk.VK_EXT_DEBUG_UTILS_EXTENSION_NAME)
            
            # Create instance
            instance_create_info = vk.VkInstanceCreateInfo(
                pApplicationInfo=app_info,
                enabledExtensionCount=len(extensions),
                ppEnabledExtensionNames=extensions,
            )
            
            self.instance = vk.vkCreateInstance(instance_create_info, None)
            logging.info("Vulkan instance created successfully")
            
            # Create surface
            self.surface = self.window.create_vulkan_surface(self.instance)
            if not self.surface:
                logging.error("Failed to create Vulkan surface")
                raise RuntimeError("Failed to create Vulkan surface")
                
            logging.info("Vulkan surface created successfully")
            
        except Exception as e:
            logging.error(f"Vulkan initialization error: {e}")
            raise
        
        # Additionally create a fallback renderer for simple 2D shapes
        self._initialize_fallback()
    
    def begin_frame(self):
        """Begin a new frame for rendering."""
        if self.sdl_renderer:
            # Clear the screen with black
            sdl2.SDL_SetRenderDrawColor(self.sdl_renderer, 0, 0, 0, 255)
            sdl2.SDL_RenderClear(self.sdl_renderer)
    
    def end_frame(self):
        """Present the rendered frame."""
        if self.sdl_renderer:
            sdl2.SDL_RenderPresent(self.sdl_renderer)
    
    def draw_rect(self, rect, color):
        """Draw a filled rectangle with the specified color."""
        if self.sdl_renderer:
            x, y, w, h = rect
            r, g, b, a = color
            
            sdl2.SDL_SetRenderDrawColor(self.sdl_renderer, r, g, b, a)
            
            # Create SDL_Rect
            sdl_rect = sdl2.SDL_Rect(int(x), int(y), int(w), int(h))
            
            # Draw filled rectangle
            sdl2.SDL_RenderFillRect(self.sdl_renderer, sdl_rect)
    
    def cleanup(self):
        """Clean up resources."""
        # Clean up SDL renderer
        if self.sdl_renderer:
            sdl2.SDL_DestroyRenderer(self.sdl_renderer)
            self.sdl_renderer = None
        
        # Clean up Vulkan resources
        if self.instance:
            if self.surface:
                vk.vkDestroySurfaceKHR(self.instance, self.surface, None)
                self.surface = None
                
            vk.vkDestroyInstance(self.instance, None)
            self.instance = None
