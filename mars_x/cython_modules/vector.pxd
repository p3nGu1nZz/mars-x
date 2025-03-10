# cython: language_level=3

cdef class Vector2:
    cdef public double x
    cdef public double y
    
    cpdef double length(self)
    cpdef Vector2 normalize(self)
    cpdef double dot(self, Vector2 other)
    cpdef Vector2 copy(self)

cdef class Vector3:
    cdef public double x
    cdef public double y
    cdef public double z
    
    cpdef double length(self)
    cpdef Vector3 normalize(self)
    cpdef double dot(self, Vector3 other)
    cpdef Vector3 cross(self, Vector3 other)
    cpdef Vector3 copy(self)

cdef class Vector4:
    cdef public double x
    cdef public double y
    cdef public double z
    cdef public double w
    
    cpdef double length(self)
    cpdef Vector4 normalize(self)
    cpdef double dot(self, Vector4 other)
    cpdef Vector4 copy(self)
