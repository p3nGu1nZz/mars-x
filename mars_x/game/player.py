"""
Player entity implementation for Mars-X.
"""
import logging
import ctypes
import sdl2
from mars_x.game.entity import Entity

class Player(Entity):
    """Represents the player entity in the game world."""
    
    def __init__(self):
        # Initialize base entity with player position
        super().__init__(x=400.0, y=300.0)
        
        # Player-specific properties
        self.width = 50
        self.height = 50
        self.speed = 300.0  # Speed in pixels per second (increased from 5.0)
        self.color = (255, 0, 0, 255)  # Red
        self.mass = 1.0
        
        logging.info(f"Player initialized at position ({self.x}, {self.y})")
    
    def start(self, world=None):
        """Initialize player in the game world."""
        # Call the parent start method to set up physics
        physics_entity = super().start(world)
        
        if physics_entity:
            # Additional player-specific physics setup
            physics_entity.mass = self.mass
            physics_entity.radius = max(self.width, self.height) / 2
            
            logging.info(f"Added player to physics system with radius {physics_entity.radius}")
        
        return physics_entity
    
    def update(self, input_manager, delta_time=1/60):
        """Update player position based on input."""
        # Handle movement based on input manager and delta time
        self.handle_input(input_manager, delta_time)
    
    def handle_input(self, input_manager, delta_time):
        """Handle player input and update position accordingly using delta time."""
        moved = False
        
        # Calculate frame-adjusted movement distance
        movement = self.speed * delta_time
        
        # Check for WASD movement
        if input_manager.is_action_active('move_forward'):
            self.y -= movement
            moved = True
            
        if input_manager.is_action_active('move_backward'):
            self.y += movement
            moved = True
            
        if input_manager.is_action_active('move_left'):
            self.x -= movement
            moved = True
            
        if input_manager.is_action_active('move_right'):
            self.x += movement
            moved = True
            
        # Log movement if any occurred (but not on every frame to avoid log spam)
        if moved and delta_time > 0.01:  # Only log occasionally
            logging.debug(f"Player moved to ({self.x:.1f}, {self.y:.1f}), delta: {delta_time:.4f}")
    
    def get_rect(self):
        """Get rectangle (x, y, width, height) for rendering."""
        # Convert center position to top-left corner for rendering
        left = self.x - (self.width / 2)
        top = self.y - (self.height / 2)
        return (left, top, self.width, self.height)
    
    def render(self, renderer):
        """Render the player using the provided renderer."""
        if not self.active:
            return
            
        # Set red color for player rectangle
        sdl2.SDL_SetRenderDrawColor(renderer, 255, 0, 0, 255)  # Red
        
        # Get player rectangle coordinates (convert from center position to top-left)
        rect = self.get_rect()
        sdl_rect = sdl2.SDL_Rect(int(rect[0]), int(rect[1]), int(rect[2]), int(rect[3]))
        
        # Draw filled rectangle
        sdl2.SDL_RenderFillRect(renderer, ctypes.byref(sdl_rect))
