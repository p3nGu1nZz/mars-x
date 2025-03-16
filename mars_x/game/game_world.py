import logging
import sdl2
from mars_x.game.player import Player

# Import the Cython physics module - no fallbacks
from mars_x.cython_modules.rigidbody import update_positions, apply_force, Entity as CythonEntity  # type: ignore

class GameWorld:
    def __init__(self, renderer):
        self.renderer = renderer
        self.entities = []
        self.rigidbody = []  # Entities that will be processed by Cython physics
        self.player = None
        self.init_world()
        logging.info("Game world initialized")
    
    def init_world(self):
        """Initialize the game world with entities including the player."""
        logging.info("Initializing game world...")
        
        # Create player entity
        self.player = Player()
        
        # Add player to entity list (for future batch processing)
        self.add_entity(self.player)
    
    def add_entity(self, entity):
        """
        Add an entity to the game world.
        If the entity has physics properties, it will also be added to the physics system.
        """
        if entity not in self.entities:
            self.entities.append(entity)
            
            # Initialize the entity and add to physics system if needed
            rigidbody = entity.start(self)
            if rigidbody:
                self.rigidbody.append(rigidbody)
                logging.debug(f"Added entity to physics system: {entity}")
            
            logging.debug(f"Added entity to game world: {entity}")
            return True
        return False
    
    def remove_entity(self, entity):
        """Remove an entity from the game world and physics system if present."""
        if entity in self.entities:
            self.entities.remove(entity)
            
            # Also remove from physics if it has a physics entity
            if hasattr(entity, 'rigidbody') and entity.rigidbody in self.rigidbody:
                self.rigidbody.remove(entity.rigidbody)
                logging.debug(f"Removed entity from physics system: {entity}")
            
            logging.debug(f"Removed entity from game world: {entity}")
            return True
        return False
    
    def update(self, input_manager, delta_time=1/60):
        """Update game state based on input and game logic."""
        # Update all entities with the current input state
        for entity in self.entities:
            if hasattr(entity, 'update'):
                entity.update(input_manager, delta_time)
                
                # Sync positions from game entity to physics entity if needed
                if hasattr(entity, 'rigidbody') and entity.rigidbody in self.rigidbody:
                    entity.rigidbody.x = entity.x
                    entity.rigidbody.y = entity.y
        
        # Update physics using Cython
        if self.rigidbody:
            update_positions(self.rigidbody, delta_time)
            
            # Sync positions from physics entities back to game entities
            for entity in self.entities:
                if hasattr(entity, 'rigidbody') and entity.rigidbody in self.rigidbody:
                    entity.x = entity.rigidbody.x
                    entity.y = entity.rigidbody.y
    
    def render(self):
        """Render the game world using the active renderer."""
        # Let each entity render itself
        for entity in self.entities:
            if hasattr(entity, 'render'):
                entity.render(self.renderer)
