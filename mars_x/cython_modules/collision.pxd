# cython: language_level=3

from mars_x.cython_modules.physics cimport Entity

# Function to check collision between two circular objects - use cpdef for Python-visible functions
cpdef bint check_collision(double x1, double y1, double r1, double x2, double y2, double r2)

# Resolve all collisions between entities
cpdef void resolve_collisions(list entities)

# Private function to handle collision response (keep as cdef for internal use)
cdef void _handle_collision(Entity entity1, Entity entity2, double restitution)
