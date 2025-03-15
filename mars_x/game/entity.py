"""
Base entity class for Mars-X.
Provides common functionality for all game entities.
"""
import logging
import uuid

class Entity:
    """Base class for all game entities."""
    
    def __init__(self, x=0.0, y=0.0):
        # Unique identifier for the entity
        self.id = str(uuid.uuid4())
        
        # Position (center of entity)
        self.x = x
        self.y = y
        
        # Whether the entity is active
        self.active = True
        
        logging.debug(f"Entity {self.id} created at ({self.x}, {self.y})")
    
    def update(self, input_manager=None, delta_time=1/60):
        """Update the entity state. Override in subclasses."""
        pass
    
    def render(self, renderer):
        """Render the entity. Override in subclasses."""
        pass
