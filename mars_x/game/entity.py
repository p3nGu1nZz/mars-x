"""
Base entity class for game objects in Mars-X.
"""
import logging
from mars_x.cython_modules.rigidbody import Entity as CythonEntity  # type: ignore

class Entity:
    """Base class for all game entities."""
    
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y
        self.active = True
        self.physics_entity = None  # Reference to the Cython physics entity
        self.width = 10.0  # Default width for collision detection
        self.height = 10.0  # Default height for collision detection
    
    def start(self, world=None):
        """
        Initialize the entity after it's added to the world.
        Override in subclasses for custom initialization.
        """
        # Always create a Cython physics entity
        physics_entity = CythonEntity()
        
        # Copy properties from game entity to physics entity
        physics_entity.x = self.x
        physics_entity.y = self.y
        physics_entity.vx = getattr(self, 'vx', 0.0)
        physics_entity.vy = getattr(self, 'vy', 0.0)
        physics_entity.mass = getattr(self, 'mass', 1.0)
        physics_entity.rotation = getattr(self, 'rotation', 0.0)
        physics_entity.active = self.active
        
        # Calculate radius from width/height if available
        physics_entity.radius = max(self.width, self.height) / 2
        
        # Store the physics entity
        self.physics_entity = physics_entity
        
        logging.debug(f"Physics entity created for {self.__class__.__name__} with radius {physics_entity.radius}")
        
        return physics_entity
    
    def update(self, input_manager, delta_time):
        """Update entity state. Override in subclasses."""
        pass
    
    def render(self, renderer):
        """Render the entity. Override in subclasses."""
        pass
