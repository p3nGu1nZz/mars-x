# cython: language_level=3
# cython: boundscheck=False
# cython: wraparound=False

import cython
from libc.math cimport sqrt

from mars_x.cython_modules.rigidbody cimport Entity
from mars_x.cython_modules.vector cimport Vector2

@cython.cdivision(True)
cpdef bint check_collision(double x1, double y1, double radius1, double x2, double y2, double radius2):
    """Check if two circular objects are colliding."""
    cdef double dx = x2 - x1
    cdef double dy = y2 - y1
    cdef double distance_sq = dx * dx + dy * dy
    cdef double combined_radius = radius1 + radius2
    
    return distance_sq <= combined_radius * combined_radius

@cython.cdivision(True)
cpdef void resolve_collisions(list entities, double response_coef=0.8):
    """
    Detect and resolve collisions between all entities in the list.
    response_coef controls the elasticity of collisions (0.0 = inelastic, 1.0 = elastic)
    """
    cdef:
        int i, j, n
        Entity entity1, entity2
        double dx, dy, distance_sq, distance, overlap
        double nx, ny  # Normal vector components
        double p  # Impulse scalar
        double mass_sum, inv_mass_sum
        
    n = len(entities)
    
    for i in range(n):
        entity1 = entities[i]
        if not entity1.active:
            continue
            
        for j in range(i+1, n):
            entity2 = entities[j]
            if not entity2.active:
                continue
                
            # Check for collision
            dx = entity2.x - entity1.x
            dy = entity2.y - entity1.y
            distance_sq = dx*dx + dy*dy
            
            # Combined radius
            combined_radius = entity1.radius + entity2.radius
            
            # Skip if not colliding
            if distance_sq > combined_radius * combined_radius:
                continue
                
            # Handle collision
            _handle_collision(entity1, entity2, response_coef)

@cython.cdivision(True)
cdef void _handle_collision(Entity entity1, Entity entity2, double response_coef):
    """Handle collision response between two entities."""
    cdef:
        double dx = entity2.x - entity1.x
        double dy = entity2.y - entity1.y
        double distance_sq = dx*dx + dy*dy
        double distance
        double overlap
        double nx, ny  # Normalized direction
        double total_mass
        double entity1_ratio, entity2_ratio
        double rvx, rvy  # Relative velocity
        double vel_along_normal
        double impulse_scalar
        double impulse_x, impulse_y
        double dot
        
    # Skip if entities are at the exact same position to avoid division by zero
    if distance_sq < 0.0001:
        # Push entities apart slightly to prevent overlap
        entity1.x -= 0.1
        entity2.x += 0.1
        return
        
    distance = sqrt(distance_sq)
    overlap = entity1.radius + entity2.radius - distance
    nx = dx / distance  # Normalized x direction
    ny = dy / distance  # Normalized y direction
        
    # Separate the entities to avoid overlap
    if entity1.mass > 0 and entity2.mass > 0:
        # Both entities have finite mass
        total_mass = entity1.mass + entity2.mass
        entity1_ratio = entity2.mass / total_mass
        entity2_ratio = entity1.mass / total_mass
        
        entity1.x -= nx * overlap * entity1_ratio
        entity1.y -= ny * overlap * entity1_ratio
        entity2.x += nx * overlap * entity2_ratio
        entity2.y += ny * overlap * entity2_ratio
        
        # Calculate relative velocity
        rvx = entity2.vx - entity1.vx
        rvy = entity2.vy - entity1.vy
        
        # Calculate velocity along the normal
        vel_along_normal = rvx * nx + rvy * ny
        
        # Do not resolve if velocities are separating
        if vel_along_normal > 0:
            return
            
        # Calculate impulse scalar
        impulse_scalar = -(1 + response_coef) * vel_along_normal
        impulse_scalar /= (1/entity1.mass) + (1/entity2.mass)
        
        # Apply impulse
        impulse_x = impulse_scalar * nx
        impulse_y = impulse_scalar * ny
        
        entity1.vx -= impulse_x / entity1.mass
        entity1.vy -= impulse_y / entity1.mass
        entity2.vx += impulse_x / entity2.mass
        entity2.vy += impulse_y / entity2.mass
    
    elif entity1.mass > 0:
        # Only entity1 has mass (entity2 is immovable)
        entity1.x -= nx * overlap
        entity1.y -= ny * overlap
        
        # Simple reflection
        dot = entity1.vx * nx + entity1.vy * ny
        entity1.vx = response_coef * (entity1.vx - 2 * dot * nx)
        entity1.vy = response_coef * (entity1.vy - 2 * dot * ny)
        
    elif entity2.mass > 0:
        # Only entity2 has mass (entity1 is immovable)
        entity2.x += nx * overlap
        entity2.y += ny * overlap
        
        # Simple reflection
        dot = entity2.vx * nx + entity2.vy * ny
        entity2.vx = response_coef * (entity2.vx - 2 * dot * nx)
        entity2.vy = response_coef * (entity2.vy - 2 * dot * ny)
