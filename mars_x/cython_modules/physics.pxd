# cython: language_level=3

cdef class Entity:
    cdef public double x
    cdef public double y
    cdef public double vx
    cdef public double vy
    cdef public double mass
    cdef public double rotation
    cdef public bint active
    cdef public double radius  # Added radius attribute for collision detection
