# cython: language_level=3
# cython: boundscheck=False
# cython: wraparound=False

import cython
from libc.math cimport sin, cos, sqrt

# Our own vector type definition
cdef struct Vector2D:
    double x
    double y

# Entity class is now defined only in physics.pxd
# Implementation of the methods goes here

def update_positions(entities, double dt=1/60.0):
    """Update physics for all entities"""
    cdef Entity entity
    
    for entity in entities:
        if entity.active:
            # Update position based on velocity
            entity.x += entity.vx * dt
            entity.y += entity.vy * dt
            
            # Apply space drag (very minimal in space)
            entity.vx *= 0.999
            entity.vy *= 0.999

@cython.cdivision(True)
cdef Vector2D vec_normalize(Vector2D v) nogil:
    """Normalize a vector to unit length"""
    cdef double length
    cdef Vector2D result
    
    length = sqrt(v.x * v.x + v.y * v.y)
    
    if length > 0:
        result.x = v.x / length
        result.y = v.y / length
    else:
        result.x = 0
        result.y = 0
    
    return result

def apply_thrust(Entity entity, double thrust_power, double direction):
    """Apply thrust to an entity in the given direction"""
    cdef:
        double rad_direction = direction * 3.14159265359 / 180.0
        double force_x = thrust_power * cos(rad_direction)
        double force_y = thrust_power * sin(rad_direction)
    
    # F = ma, so a = F/m
    entity.vx += force_x / entity.mass
    entity.vy += force_y / entity.mass
