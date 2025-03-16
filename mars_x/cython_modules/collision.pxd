# cython: language_level=3

from mars_x.cython_modules.rigidbody cimport Entity

cpdef bint check_collision(double x1, double y1, double radius1, double x2, double y2, double radius2)
cpdef void resolve_collisions(list entities, double response_coef=*)
cdef void _handle_collision(Entity entity1, Entity entity2, double response_coef)
