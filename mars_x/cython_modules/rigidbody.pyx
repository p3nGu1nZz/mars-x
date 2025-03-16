# cython: language_level=3
# cython: boundscheck=False
# cython: wraparound=False

import cython

cimport libc.math  # type: ignore
from libc.math cimport sin, cos, sqrt, M_PI  # type: ignore

# Import our vector class
from mars_x.cython_modules.vector cimport Vector2

# Our own vector type definition
cdef struct Vector2D:
    double x
    double y

# TODO: Move Entity class into its own file.
cdef class Entity:
    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.vx = 0.0
        self.vy = 0.0
        self.mass = 1.0
        self.rotation = 0.0
        self.active = True
        self.radius = 0.0

@cython.cdivision(True)
cpdef void update_positions(list entities, double dt=1/60.0):
    """
    Update positions of physics entities based on their velocities.
    This is optimized with Cython for performance.
    """
    cdef int i
    cdef Entity entity
    
    for i in range(len(entities)):
        entity = entities[i]
        if entity.active:
            entity.x += entity.vx * dt
            entity.y += entity.vy * dt
            
            # Apply space drag (very minimal in space)
            entity.vx *= 0.999
            entity.vy *= 0.999

@cython.cdivision(True)
cdef Vector2D vec_normalize(Vector2D v) nogil:
    """
    Normalize a vector to unit length more efficiently by computing
    the inverse square root only once.
    """
    cdef double length_sq, inv_length
    cdef Vector2D result
    
    length_sq = v.x * v.x + v.y * v.y
    
    if length_sq > 0:
        inv_length = 1.0 / sqrt(length_sq)
        result.x = v.x * inv_length
        result.y = v.y * inv_length
    else:
        result.x = 0
        result.y = 0
    
    return result

@cython.cdivision(True)
cdef Vector2D vec_direction(Vector2D v, double max_length) nogil:
    """
    Get a vector's direction without using square root.
    This is faster but doesn't produce a unit vector.
    """
    cdef double length_sq
    cdef Vector2D result
    
    length_sq = v.x * v.x + v.y * v.y
    
    if length_sq > 0:
        # Just return the original vector direction
        result.x = v.x
        result.y = v.y
    else:
        result.x = 0
        result.y = 0
    
    return result

@cython.cdivision(True)
cpdef void apply_force(Entity entity, Vector2 force):
    """
    Apply a force vector to an entity.
    Force will be divided by mass to produce acceleration (F = ma).
    """
    if entity.mass == 0:
        return
    
    # F = ma, so a = F/m
    entity.vx += force.x / entity.mass
    entity.vy += force.y / entity.mass

@cython.cdivision(True)
cpdef void apply_torque(Entity entity, double torque):
    """
    Apply a torque to rotate the entity.
    Positive values rotate clockwise, negative counter-clockwise.
    """
    if entity.mass == 0:
        return
    
    # Simple model: angular_acceleration = torque / mass
    # Add to rotation (in radians)
    entity.rotation += torque / entity.mass
    
    # Normalize rotation to 0-2π radians
    while entity.rotation >= 2*M_PI:
        entity.rotation -= 2*M_PI
    while entity.rotation < 0.0:
        entity.rotation += 2*M_PI
