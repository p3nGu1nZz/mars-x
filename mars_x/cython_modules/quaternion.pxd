# cython: language_level=3

from mars_x.cython_modules.vector cimport Vector3, Vector4
from mars_x.cython_modules.matrix cimport Matrix4

cdef class Quaternion:
    cdef public double x
    cdef public double y
    cdef public double z
    cdef public double w
    
    cpdef double length(self)
    cpdef Quaternion normalize(self)
    cpdef Quaternion conjugate(self)
    cpdef Quaternion inverse(self)
    cpdef Vector3 rotate_vector3(self, Vector3 v)
    cpdef Matrix4 to_rotation_matrix(self)
    cpdef Quaternion copy(self)
    
    @staticmethod
    cdef Quaternion identity()
    
    @staticmethod
    cdef Quaternion from_axis_angle(Vector3 axis, double angle)
    
    @staticmethod
    cdef Quaternion from_euler_angles(double x, double y, double z)
    
    @staticmethod
    cdef Quaternion from_matrix(Matrix4 m)
    
    @staticmethod
    cdef Quaternion slerp(Quaternion a, Quaternion b, double t)
