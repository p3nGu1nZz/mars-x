import sdl2
import logging

class InputManager:
    def __init__(self):
        self.event = sdl2.SDL_Event()
        self.keys = sdl2.SDL_GetKeyboardState(None)
        self.mouse_x = 0
        self.mouse_y = 0
        self.mouse_buttons = {}
        
        # Add handling for game actions - remove arrow key movements for simplicity
        self.actions = {
            'move_forward': False,  # W key
            'move_backward': False, # S key
            'move_left': False,     # A key
            'move_right': False,    # D key
            'jump': False,
            'fire': False,
            'toggle_fullscreen': False,
            'open_settings': False, # Add a new action for opening settings
            'quit': False
        }
        
        # Key mappings for game actions - remove arrow key mappings
        self.key_mappings = {
            'move_forward': sdl2.SDLK_w,
            'move_backward': sdl2.SDLK_s,
            'move_left': sdl2.SDLK_a,
            'move_right': sdl2.SDLK_d,
            'jump': sdl2.SDLK_SPACE,
            'fire': sdl2.SDLK_LCTRL,
            'toggle_fullscreen': sdl2.SDLK_F11,
            'open_settings': sdl2.SDLK_ESCAPE,  # Map Escape to open_settings instead of quit
            'quit': None  # Remove the direct key mapping for quit
        }
        
        # Track which keys were just pressed this frame (for one-time actions)
        self.key_just_pressed = {action: False for action in self.actions}
    
    def process_input(self):
        """Process all pending SDL events and update input state."""
        quit_requested = False
        
        # Reset one-time actions
        for action in self.key_just_pressed:
            self.key_just_pressed[action] = False
        
        while sdl2.SDL_PollEvent(self.event):
            # Update mouse position
            if self.event.type in (sdl2.SDL_MOUSEMOTION, sdl2.SDL_MOUSEBUTTONDOWN, sdl2.SDL_MOUSEBUTTONUP):
                self.mouse_x = self.event.motion.x
                self.mouse_y = self.event.motion.y
                logging.debug(f"Mouse position: ({self.mouse_x}, {self.mouse_y})")
            
            # Handle window events
            if self.event.type == sdl2.SDL_WINDOWEVENT:
                if self.event.window.event == sdl2.SDL_WINDOWEVENT_RESIZED:
                    logging.info(f"Window resized to {self.event.window.data1}x{self.event.window.data2}")
            
            # Update mouse button state
            if self.event.type == sdl2.SDL_MOUSEBUTTONDOWN:
                self.mouse_buttons[self.event.button.button] = True
                logging.debug(f"Mouse button {self.event.button.button} pressed")
            elif self.event.type == sdl2.SDL_MOUSEBUTTONUP:
                self.mouse_buttons[self.event.button.button] = False
                logging.debug(f"Mouse button {self.event.button.button} released")
                
            # Process key presses and update action states
            if self.event.type == sdl2.SDL_KEYDOWN:
                key = self.event.key.keysym.sym
                logging.debug(f"Key pressed: {key}")
                
                for action, mapped_key in self.key_mappings.items():
                    if key == mapped_key:
                        # For continuous actions
                        self.actions[action] = True
                        
                        # For one-time actions (like toggling fullscreen)
                        self.key_just_pressed[action] = True
                        
                        logging.debug(f"Action '{action}' activated")
                
            # Process key releases
            elif self.event.type == sdl2.SDL_KEYUP:
                key = self.event.key.keysym.sym
                logging.debug(f"Key released: {key}")
                
                for action, mapped_key in self.key_mappings.items():
                    if key == mapped_key:
                        self.actions[action] = False
                        logging.debug(f"Action '{action}' deactivated")
            
            # Handle window close event (X button)
            if self.event.type == sdl2.SDL_QUIT:
                self.actions['quit'] = True
                quit_requested = True
                logging.debug("Quit requested via window close")
        
        # Update keyboard state
        self.keys = sdl2.SDL_GetKeyboardState(None)
        
        # Check if quit was requested by any method - now only window close triggers this
        if self.actions['quit']:
            quit_requested = True
            
        # Log active movement actions for debugging
        active_moves = [a for a in ['move_forward', 'move_backward', 'move_left', 'move_right'] if self.actions[a]]
        if active_moves:
            logging.debug(f"Movement actions: {', '.join(active_moves)}")
            
        return quit_requested
    
    def is_key_pressed(self, key):
        """Check if a key is currently pressed."""
        return self.keys[key]
    
    def is_mouse_button_pressed(self, button):
        """Check if a mouse button is currently pressed."""
        return self.mouse_buttons.get(button, False)
    
    def get_mouse_position(self):
        """Get the current mouse position."""
        return (self.mouse_x, self.mouse_y)
    
    def is_action_active(self, action):
        """Check if a game action is currently active."""
        return self.actions.get(action, False)
    
    def is_action_just_pressed(self, action):
        """Check if a game action was just pressed this frame (for one-time actions)."""
        return self.key_just_pressed.get(action, False)
    
    def get_active_actions(self):
        """Get a dictionary of all active actions."""
        return {action: state for action, state in self.actions.items() if state}
