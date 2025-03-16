# cython: language_level=3

# Import our vector class
from mars_x.cython_modules.vector cimport Vector2

# Vector struct declaration
cdef struct Vector2D:
    double x
    double y

cdef class Entity:
    cdef public double x
    cdef public double y
    cdef public double vx
    cdef public double vy
    cdef public double mass
    cdef public double rotation
    cdef public bint active
    cdef public double radius

# Function declarations
cpdef void update_positions(list entities, double dt=*)
cpdef void apply_force(Entity entity, Vector2 force)
cpdef void apply_torque(Entity entity, double torque)
cdef Vector2D vec_normalize(Vector2D v) nogil
cdef Vector2D vec_direction(Vector2D v, double max_length) nogil
