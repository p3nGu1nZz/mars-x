import sdl2

class InputManager:
    def __init__(self):
        self.event = sdl2.SDL_Event()
        self.keys = sdl2.SDL_GetKeyboardState(None)
        self.mouse_x = 0
        self.mouse_y = 0
        self.mouse_buttons = {}
    
    def get_events(self):
        """Process all pending SDL events and return them."""
        events = []
        while sdl2.SDL_PollEvent(self.event):
            # Update mouse position
            if self.event.type in (sdl2.SDL_MOUSEMOTION, sdl2.SDL_MOUSEBUTTONDOWN, sdl2.SDL_MOUSEBUTTONUP):
                self.mouse_x = self.event.motion.x
                self.mouse_y = self.event.motion.y
            
            # Update mouse button state
            if self.event.type == sdl2.SDL_MOUSEBUTTONDOWN:
                self.mouse_buttons[self.event.button.button] = True
            elif self.event.type == sdl2.SDL_MOUSEBUTTONUP:
                self.mouse_buttons[self.event.button.button] = False
            
            events.append(self.event)
        
        return events
    
    def is_key_pressed(self, key):
        """Check if a key is currently pressed."""
        return self.keys[key]
    
    def is_mouse_button_pressed(self, button):
        """Check if a mouse button is currently pressed."""
        return self.mouse_buttons.get(button, False)
    
    def get_mouse_position(self):
        """Get the current mouse position."""
        return (self.mouse_x, self.mouse_y)
