# cython: language_level=3
# cython: boundscheck=False
# cython: wraparound=False

import cython
from libc.math cimport sqrt, pow
# Import Entity as an extension type
from mars_x.cython_modules.physics cimport Entity

@cython.cdivision(True)
def check_collision(double x1, double y1, double r1, double x2, double y2, double r2):
    """Check collision between two circular objects"""
    cdef:
        double distance_sq
        double dx = x2 - x1
        double dy = y2 - y1
        
    # Squared distance (avoids costly square root)
    distance_sq = dx * dx + dy * dy
    
    # If distance squared is less than the squared sum of radii, there's a collision
    return distance_sq <= (r1 + r2) * (r1 + r2)

def resolve_collisions(entities):
    """Resolve all collisions between entities"""
    cdef:
        int i, j
        int n = len(entities)
        double response_coef = 0.8  # Coefficient of restitution
        double radius1, radius2  # We need to get radius from entities
        
    for i in range(n):
        for j in range(i+1, n):
            # Using a 'radius' attribute that would need to be added to Entity
            radius1 = getattr(entities[i], 'radius', 1.0)
            radius2 = getattr(entities[j], 'radius', 1.0)
            
            if check_collision(entities[i].x, entities[i].y, radius1, 
                              entities[j].x, entities[j].y, radius2):
                # Collision found, calculate response
                _handle_collision(entities[i], entities[j], response_coef)

@cython.cdivision(True)
cdef void _handle_collision(Entity entity1, Entity entity2, double restitution):
    """Handle collision response between two entities"""
    cdef:
        double dx = entity2.x - entity1.x
        double dy = entity2.y - entity1.y
        double distance = sqrt(dx * dx + dy * dy)
        double nx, ny  # Normalized collision normal
        
        # Relative velocity
        double dvx = entity2.vx - entity1.vx
        double dvy = entity2.vy - entity1.vy
        
        # Relative velocity along collision normal
        double vnorm
        
        # Impulse scalar
        double impulse
        double im1 = 1.0 / entity1.mass  # Inverse mass
        double im2 = 1.0 / entity2.mass  # Inverse mass
        
    # Avoid division by zero
    if distance == 0:
        nx = 0
        ny = 1
    else:
        nx = dx / distance
        ny = dy / distance
    
    # Relative velocity along normal
    vnorm = dvx * nx + dvy * ny
    
    # If objects are moving apart, don't apply impulse
    if vnorm > 0:
        return
    
    # Calculate impulse scalar
    impulse = -(1.0 + restitution) * vnorm / (im1 + im2)
    
    # Apply impulse
    entity1.vx -= impulse * nx * im1
    entity1.vy -= impulse * ny * im1
    entity2.vx += impulse * nx * im2
    entity2.vy += impulse * ny * im2
