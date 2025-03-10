# cython: language_level=3

from mars_x.cython_modules.vector cimport Vector3, Vector4

cdef class Matrix4:
    # Store the matrix as flat array for better memory access patterns
    cdef public double[16] data
    
    cpdef Matrix4 transpose(self)
    cpdef double determinant(self)
    cpdef Matrix4 inverse(self)
    cpdef Matrix4 copy(self)
    cpdef Vector4 transform_vector4(self, Vector4 v)
    cpdef Vector3 transform_vector3(self, Vector3 v)
    
    @staticmethod
    cdef Matrix4 identity()
    
    @staticmethod
    cdef Matrix4 translation(double x, double y, double z)
    
    @staticmethod
    cdef Matrix4 scaling(double x, double y, double z)
    
    @staticmethod
    cdef Matrix4 rotation_x(double angle_rad)
    
    @staticmethod
    cdef Matrix4 rotation_y(double angle_rad)
    
    @staticmethod
    cdef Matrix4 rotation_z(double angle_rad)
    
    @staticmethod
    cdef Matrix4 perspective(double fov_y_rad, double aspect_ratio, double near_z, double far_z)
    
    @staticmethod
    cdef Matrix4 orthographic(double left, double right, double bottom, double top, double near_z, double far_z)
