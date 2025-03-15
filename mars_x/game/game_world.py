import logging
from mars_x.game.player import Player

class GameWorld:
    def __init__(self, renderer):
        self.renderer = renderer
        self.entities = []
        self.player = None
        self.init_world()
        logging.info("Game world initialized")
    
    def init_world(self):
        """Initialize the game world with entities including the player."""
        logging.info("Initializing game world...")
        
        # Create player entity
        self.player = Player()
        
        # Add player to entity list (for future batch processing)
        self.entities.append(self.player)
    
    def update(self, input_manager, delta_time=1/60):
        """Update game state based on input and game logic."""
        # Update all entities with the current delta time
        for entity in self.entities:
            if hasattr(entity, 'update'):
                entity.update(input_manager, delta_time)
    
    def render(self):
        """Render the game world using the active renderer."""
        # Let each entity render itself
        for entity in self.entities:
            if hasattr(entity, 'render'):
                entity.render(self.renderer)
