# cython: language_level=3
# cython: boundscheck=False
# cython: wraparound=False

import cython
from libc.math cimport sin, cos, tan
from mars_x.cython_modules.vector cimport Vector3, Vector4

# Define array indices for clearer access
# row-major order: m[row][column]
# flat array: m[row * 4 + column]
cdef enum MatrixIndex:
    M00 = 0   # Row 0, Column 0
    M01 = 1   # Row 0, Column 1
    M02 = 2   # Row 0, Column 2
    M03 = 3   # Row 0, Column 3
    M10 = 4   # Row 1, Column 0
    M11 = 5   # Row 1, Column 1
    M12 = 6   # Row 1, Column 2
    M13 = 7   # Row 1, Column 3
    M20 = 8   # Row 2, Column 0
    M21 = 9   # Row 2, Column 1
    M22 = 10  # Row 2, Column 2
    M23 = 11  # Row 2, Column 3
    M30 = 12  # Row 3, Column 0
    M31 = 13  # Row 3, Column 1
    M32 = 14  # Row 3, Column 2
    M33 = 15  # Row 3, Column 3

cdef class Matrix4:
    def __init__(self):
        # Initialize as identity matrix
        self.data = [
            1.0, 0.0, 0.0, 0.0,  # Row 0
            0.0, 1.0, 0.0, 0.0,  # Row 1
            0.0, 0.0, 1.0, 0.0,  # Row 2
            0.0, 0.0, 0.0, 1.0   # Row 3
        ]
    
    def __repr__(self):
        # Pretty print the matrix
        cdef str result = "Matrix4(\n"
        for i in range(4):
            result += "  ["
            for j in range(4):
                result += f"{self.data[i * 4 + j]:8.4f}"
                if j < 3:
                    result += ", "
            result += "]\n"
        result += ")"
        return result
    
    def __getitem__(self, tuple idx):
        cdef int row = idx[0]
        cdef int col = idx[1]
        return self.data[row * 4 + col]
    
    def __setitem__(self, tuple idx, double value):
        cdef int row = idx[0]
        cdef int col = idx[1]
        self.data[row * 4 + col] = value
    
    def __mul__(Matrix4 self, value):
        # Matrix-Matrix multiplication
        cdef Matrix4 other
        cdef Matrix4 result
        cdef int i, j, k
        cdef double scalar
        
        if isinstance(value, Matrix4):
            other = value
            result = Matrix4()
            
            for i in range(4):
                for j in range(4):
                    result.data[i * 4 + j] = 0
                    for k in range(4):
                        result.data[i * 4 + j] += self.data[i * 4 + k] * other.data[k * 4 + j]
            
            return result
        # Matrix-Scalar multiplication
        elif isinstance(value, (int, float)):
            scalar = value
            result = Matrix4()
            
            for i in range(16):
                result.data[i] = self.data[i] * scalar
            
            return result
        else:
            return NotImplemented
    
    cpdef Matrix4 transpose(self):
        """Returns the transpose of this matrix"""
        cdef Matrix4 result = Matrix4()
        cdef int i, j
        
        for i in range(4):
            for j in range(4):
                result.data[i * 4 + j] = self.data[j * 4 + i]
                
        return result
    
    cpdef double determinant(self):
        """Calculate the determinant of this matrix"""
        # Compute cofactors for the first row
        cdef double cofactor00 = (
            self.data[<int>M11] * (self.data[<int>M22] * self.data[<int>M33] - self.data[<int>M23] * self.data[<int>M32]) -
            self.data[<int>M12] * (self.data[<int>M21] * self.data[<int>M33] - self.data[<int>M23] * self.data[<int>M31]) +
            self.data[<int>M13] * (self.data[<int>M21] * self.data[<int>M32] - self.data[<int>M22] * self.data[<int>M31])
        )
        
        cdef double cofactor01 = (
            self.data[<int>M10] * (self.data[<int>M22] * self.data[<int>M33] - self.data[<int>M23] * self.data[<int>M32]) -
            self.data[<int>M12] * (self.data[<int>M20] * self.data[<int>M33] - self.data[<int>M23] * self.data[<int>M30]) +
            self.data[<int>M13] * (self.data[<int>M20] * self.data[<int>M32] - self.data[<int>M22] * self.data[<int>M30])
        )
        
        cdef double cofactor02 = (
            self.data[<int>M10] * (self.data[<int>M21] * self.data[<int>M33] - self.data[<int>M23] * self.data[<int>M31]) -
            self.data[<int>M11] * (self.data[<int>M20] * self.data[<int>M33] - self.data[<int>M23] * self.data[<int>M30]) +
            self.data[<int>M13] * (self.data[<int>M20] * self.data[<int>M31] - self.data[<int>M21] * self.data[<int>M30])
        )
        
        cdef double cofactor03 = (
            self.data[<int>M10] * (self.data[<int>M21] * self.data[<int>M32] - self.data[<int>M22] * self.data[<int>M31]) -
            self.data[<int>M11] * (self.data[<int>M20] * self.data[<int>M32] - self.data[<int>M22] * self.data[<int>M30]) +
            self.data[<int>M12] * (self.data[<int>M20] * self.data[<int>M31] - self.data[<int>M21] * self.data[<int>M30])
        )
        
        # Compute determinant using the first row of cofactors
        return (
            self.data[<int>M00] * cofactor00 -
            self.data[<int>M01] * cofactor01 +
            self.data[<int>M02] * cofactor02 -
            self.data[<int>M03] * cofactor03
        )
    
    cpdef Matrix4 inverse(self):
        """Calculate the inverse of this matrix"""
        cdef double det = self.determinant()
        
        # Check if the matrix is invertible
        if abs(det) < 1e-10:
            raise ValueError("Matrix is not invertible (determinant is close to zero)")
        
        cdef double inv_det = 1.0 / det
        cdef Matrix4 result = Matrix4()
        
        # Compute adjugate matrix and multiply by inverse determinant
        # Row 0
        result.data[<int>M00] = inv_det * (
            self.data[<int>M11] * (self.data[<int>M22] * self.data[<int>M33] - self.data[<int>M23] * self.data[<int>M32]) -
            self.data[<int>M12] * (self.data[<int>M21] * self.data[<int>M33] - self.data[<int>M23] * self.data[<int>M31]) +
            self.data[<int>M13] * (self.data[<int>M21] * self.data[<int>M32] - self.data[<int>M22] * self.data[<int>M31])
        )
        
        result.data[<int>M01] = -inv_det * (
            self.data[<int>M01] * (self.data[<int>M22] * self.data[<int>M33] - self.data[<int>M23] * self.data[<int>M32]) -
            self.data[<int>M02] * (self.data[<int>M21] * self.data[<int>M33] - self.data[<int>M23] * self.data[<int>M31]) +
            self.data[<int>M03] * (self.data[<int>M21] * self.data[<int>M32] - self.data[<int>M22] * self.data[<int>M31])
        )
        
        result.data[<int>M02] = inv_det * (
            self.data[<int>M01] * (self.data[<int>M12] * self.data[<int>M33] - self.data[<int>M13] * self.data[<int>M32]) -
            self.data[<int>M02] * (self.data[<int>M11] * self.data[<int>M33] - self.data[<int>M13] * self.data[<int>M31]) +
            self.data[<int>M03] * (self.data[<int>M11] * self.data[<int>M32] - self.data[<int>M12] * self.data[<int>M31])
        )
        
        result.data[<int>M03] = -inv_det * (
            self.data[<int>M01] * (self.data[<int>M12] * self.data[<int>M23] - self.data[<int>M13] * self.data[<int>M22]) -
            self.data[<int>M02] * (self.data[<int>M11] * self.data[<int>M23] - self.data[<int>M13] * self.data[<int>M21]) +
            self.data[<int>M03] * (self.data[<int>M11] * self.data[<int>M22] - self.data[<int>M12] * self.data[<int>M21])
        )
        
        # Row 1
        result.data[<int>M10] = -inv_det * (
            self.data[<int>M10] * (self.data[<int>M22] * self.data[<int>M33] - self.data[<int>M23] * self.data[<int>M32]) -
            self.data[<int>M12] * (self.data[<int>M20] * self.data[<int>M33] - self.data[<int>M23] * self.data[<int>M30]) +
            self.data[<int>M13] * (self.data[<int>M20] * self.data[<int>M32] - self.data[<int>M22] * self.data[<int>M30])
        )
        
        result.data[<int>M11] = inv_det * (
            self.data[<int>M00] * (self.data[<int>M22] * self.data[<int>M33] - self.data[<int>M23] * self.data[<int>M32]) -
            self.data[<int>M02] * (self.data[<int>M20] * self.data[<int>M33] - self.data[<int>M23] * self.data[<int>M30]) +
            self.data[<int>M03] * (self.data[<int>M20] * self.data[<int>M32] - self.data[<int>M22] * self.data[<int>M30])
        )
        
        result.data[<int>M12] = -inv_det * (
            self.data[<int>M00] * (self.data[<int>M12] * self.data[<int>M33] - self.data[<int>M13] * self.data[<int>M32]) -
            self.data[<int>M02] * (self.data[<int>M10] * self.data[<int>M33] - self.data[<int>M13] * self.data[<int>M30]) +
            self.data[<int>M03] * (self.data[<int>M10] * self.data[<int>M32] - self.data[<int>M12] * self.data[<int>M30])
        )
        
        result.data[<int>M13] = inv_det * (
            self.data[<int>M00] * (self.data[<int>M12] * self.data[<int>M23] - self.data[<int>M13] * self.data[<int>M22]) -
            self.data[<int>M02] * (self.data[<int>M10] * self.data[<int>M23] - self.data[<int>M13] * self.data[<int>M20]) +
            self.data[<int>M03] * (self.data[<int>M10] * self.data[<int>M22] - self.data[<int>M12] * self.data[<int>M20])
        )
        
        # Row 2
        result.data[<int>M20] = inv_det * (
            self.data[<int>M10] * (self.data[<int>M21] * self.data[<int>M33] - self.data[<int>M23] * self.data[<int>M31]) -
            self.data[<int>M11] * (self.data[<int>M20] * self.data[<int>M33] - self.data[<int>M23] * self.data[<int>M30]) +
            self.data[<int>M13] * (self.data[<int>M20] * self.data[<int>M31] - self.data[<int>M21] * self.data[<int>M30])
        )
        
        result.data[<int>M21] = -inv_det * (
            self.data[<int>M00] * (self.data[<int>M21] * self.data[<int>M33] - self.data[<int>M23] * self.data[<int>M31]) -
            self.data[<int>M01] * (self.data[<int>M20] * self.data[<int>M33] - self.data[<int>M23] * self.data[<int>M30]) +
            self.data[<int>M03] * (self.data[<int>M20] * self.data[<int>M31] - self.data[<int>M21] * self.data[<int>M30])
        )
        
        result.data[<int>M22] = inv_det * (
            self.data[<int>M00] * (self.data[<int>M11] * self.data[<int>M33] - self.data[<int>M13] * self.data[<int>M31]) -
            self.data[<int>M01] * (self.data[<int>M10] * self.data[<int>M33] - self.data[<int>M13] * self.data[<int>M30]) +
            self.data[<int>M03] * (self.data[<int>M10] * self.data[<int>M31] - self.data[<int>M11] * self.data[<int>M30])
        )
        
        result.data[<int>M23] = -inv_det * (
            self.data[<int>M00] * (self.data[<int>M11] * self.data[<int>M23] - self.data[<int>M13] * self.data[<int>M21]) -
            self.data[<int>M01] * (self.data[<int>M10] * self.data[<int>M23] - self.data[<int>M13] * self.data[<int>M20]) +
            self.data[<int>M03] * (self.data[<int>M10] * self.data[<int>M21] - self.data[<int>M11] * self.data[<int>M20])
        )
        
        # Row 3
        result.data[<int>M30] = -inv_det * (
            self.data[<int>M10] * (self.data[<int>M21] * self.data[<int>M32] - self.data[<int>M22] * self.data[<int>M31]) -
            self.data[<int>M11] * (self.data[<int>M20] * self.data[<int>M32] - self.data[<int>M22] * self.data[<int>M30]) +
            self.data[<int>M12] * (self.data[<int>M20] * self.data[<int>M31] - self.data[<int>M21] * self.data[<int>M30])
        )
        
        result.data[<int>M31] = inv_det * (
            self.data[<int>M00] * (self.data[<int>M21] * self.data[<int>M32] - self.data[<int>M22] * self.data[<int>M31]) -
            self.data[<int>M01] * (self.data[<int>M20] * self.data[<int>M32] - self.data[<int>M22] * self.data[<int>M30]) +
            self.data[<int>M02] * (self.data[<int>M20] * self.data[<int>M31] - self.data[<int>M21] * self.data[<int>M30])
        )
        
        result.data[<int>M32] = -inv_det * (
            self.data[<int>M00] * (self.data[<int>M11] * self.data[<int>M32] - self.data[<int>M12] * self.data[<int>M31]) -
            self.data[<int>M01] * (self.data[<int>M10] * self.data[<int>M32] - self.data[<int>M12] * self.data[<int>M30]) +
            self.data[<int>M02] * (self.data[<int>M10] * self.data[<int>M31] - self.data[<int>M11] * self.data[<int>M30])
        )
        
        result.data[<int>M33] = inv_det * (
            self.data[<int>M00] * (self.data[<int>M11] * self.data[<int>M22] - self.data[<int>M12] * self.data[<int>M21]) -
            self.data[<int>M01] * (self.data[<int>M10] * self.data[<int>M22] - self.data[<int>M12] * self.data[<int>M20]) +
            self.data[<int>M02] * (self.data[<int>M10] * self.data[<int>M21] - self.data[<int>M11] * self.data[<int>M20])
        )
        
        return result
    
    cpdef Matrix4 copy(self):
        """Returns a copy of this matrix"""
        cdef Matrix4 result = Matrix4()
        cdef int i
        
        for i in range(16):
            result.data[i] = self.data[i]
            
        return result
    
    cpdef Vector4 transform_vector4(self, Vector4 v):
        """Transform a 4D vector by this matrix"""
        cdef double x = self.data[<int>M00] * v.x + self.data[<int>M01] * v.y + self.data[<int>M02] * v.z + self.data[<int>M03] * v.w
        cdef double y = self.data[<int>M10] * v.x + self.data[<int>M11] * v.y + self.data[<int>M12] * v.z + self.data[<int>M13] * v.w
        cdef double z = self.data[<int>M20] * v.x + self.data[<int>M21] * v.y + self.data[<int>M22] * v.z + self.data[<int>M23] * v.w
        cdef double w = self.data[<int>M30] * v.x + self.data[<int>M31] * v.y + self.data[<int>M32] * v.z + self.data[<int>M33] * v.w
        
        return Vector4(x, y, z, w)
    
    cpdef Vector3 transform_vector3(self, Vector3 v):
        """Transform a 3D vector by this matrix (assuming w=1)"""
        cdef double x = self.data[<int>M00] * v.x + self.data[<int>M01] * v.y + self.data[<int>M02] * v.z + self.data[<int>M03]
        cdef double y = self.data[<int>M10] * v.x + self.data[<int>M11] * v.y + self.data[<int>M12] * v.z + self.data[<int>M13]
        cdef double z = self.data[<int>M20] * v.x + self.data[<int>M21] * v.y + self.data[<int>M22] * v.z + self.data[<int>M23]
        cdef double w = self.data[<int>M30] * v.x + self.data[<int>M31] * v.y + self.data[<int>M32] * v.z + self.data[<int>M33]
        
        # Perspective division if w is not 1
        if w != 1.0 and w != 0.0:
            x /= w
            y /= w
            z /= w
        
        return Vector3(x, y, z)
    
    # Replace Python static methods with cdef static methods
    @staticmethod
    cdef Matrix4 identity():
        """Create an identity matrix"""
        return Matrix4()
    
    @staticmethod
    cdef Matrix4 translation(double x, double y, double z):
        """Create a translation matrix"""
        cdef Matrix4 m = Matrix4()
        m.data[<int>M03] = x
        m.data[<int>M13] = y
        m.data[<int>M23] = z
        return m
    
    @staticmethod
    cdef Matrix4 scaling(double x, double y, double z):
        """Create a scaling matrix"""
        cdef Matrix4 m = Matrix4()
        m.data[<int>M00] = x
        m.data[<int>M11] = y
        m.data[<int>M22] = z
        return m
    
    @staticmethod
    cdef Matrix4 rotation_x(double angle_rad):
        """Create a rotation matrix around the X axis"""
        cdef Matrix4 m = Matrix4()
        cdef double c = cos(angle_rad)
        cdef double s = sin(angle_rad)
        
        m.data[<int>M11] = c
        m.data[<int>M12] = -s
        m.data[<int>M21] = s
        m.data[<int>M22] = c
        
        return m
    
    @staticmethod
    cdef Matrix4 rotation_y(double angle_rad):
        """Create a rotation matrix around the Y axis"""
        cdef Matrix4 m = Matrix4()
        cdef double c = cos(angle_rad)
        cdef double s = sin(angle_rad)
        
        m.data[<int>M00] = c
        m.data[<int>M02] = s
        m.data[<int>M20] = -s
        m.data[<int>M22] = c
        
        return m
    
    @staticmethod
    cdef Matrix4 rotation_z(double angle_rad):
        """Create a rotation matrix around the Z axis"""
        cdef Matrix4 m = Matrix4()
        cdef double c = cos(angle_rad)
        cdef double s = sin(angle_rad)
        
        m.data[<int>M00] = c
        m.data[<int>M01] = -s
        m.data[<int>M10] = s
        m.data[<int>M11] = c
        
        return m
    
    @staticmethod
    cdef Matrix4 perspective(double fov_y_rad, double aspect_ratio, double near_z, double far_z):
        """Create a perspective projection matrix"""
        cdef Matrix4 m = Matrix4()
        cdef double tan_half_fov = tan(fov_y_rad / 2.0)
        cdef double f = 1.0 / tan_half_fov  # focal length
        cdef double range_inv = 1.0 / (near_z - far_z)
        
        m.data[<int>M00] = f / aspect_ratio
        m.data[<int>M11] = f
        m.data[<int>M22] = (far_z + near_z) * range_inv
        m.data[<int>M23] = 2.0 * far_z * near_z * range_inv
        m.data[<int>M32] = -1.0  # Set w = -z for perspective division
        m.data[<int>M33] = 0.0
        
        return m
    
    @staticmethod
    cdef Matrix4 orthographic(double left, double right, double bottom, double top, 
                          double near_z, double far_z):
        """Create an orthographic projection matrix"""
        cdef Matrix4 m = Matrix4()
        cdef double width = right - left
        cdef double height = top - bottom
        cdef double depth = far_z - near_z
        
        m.data[<int>M00] = 2.0 / width
        m.data[<int>M03] = -(right + left) / width
        m.data[<int>M11] = 2.0 / height
        m.data[<int>M13] = -(top + bottom) / height
        m.data[<int>M22] = -2.0 / depth
        m.data[<int>M23] = -(far_z + near_z) / depth
        
        return m
    
    # Public wrapper methods for the cdef static methods
    @staticmethod
    def create_identity():
        """Public wrapper for identity()"""
        return Matrix4.identity()
    
    @staticmethod
    def create_translation(x, y, z):
        """Public wrapper for translation()"""
        return Matrix4.translation(x, y, z)
    
    @staticmethod
    def create_scaling(x, y, z):
        """Public wrapper for scaling()"""
        return Matrix4.scaling(x, y, z)
    
    @staticmethod
    def create_rotation_x(angle_rad):
        """Public wrapper for rotation_x()"""
        return Matrix4.rotation_x(angle_rad)
    
    @staticmethod
    def create_rotation_y(angle_rad):
        """Public wrapper for rotation_y()"""
        return Matrix4.rotation_y(angle_rad)
    
    @staticmethod
    def create_rotation_z(angle_rad):
        """Public wrapper for rotation_z()"""
        return Matrix4.rotation_z(angle_rad)
    
    @staticmethod
    def create_perspective(fov_y_rad, aspect_ratio, near_z, far_z):
        """Public wrapper for perspective()"""
        return Matrix4.perspective(fov_y_rad, aspect_ratio, near_z, far_z)
    
    @staticmethod
    def create_orthographic(left, right, bottom, top, near_z, far_z):
        """Public wrapper for orthographic()"""
        return Matrix4.orthographic(left, right, bottom, top, near_z, far_z)
