# cython: language_level=3
# cython: boundscheck=False
# cython: wraparound=False

import cython
from libc.math cimport sin, cos, acos, sqrt
from mars_x.cython_modules.vector cimport Vector3, Vector4
from mars_x.cython_modules.matrix cimport Matrix4

cdef class Quaternion:
    """
    Quaternion class for 3D rotations
    """
    def __init__(self, double x=0.0, double y=0.0, double z=0.0, double w=1.0):
        """Initialize quaternion with given components, defaults to identity"""
        self.x = x
        self.y = y
        self.z = z
        self.w = w
    
    def __repr__(self):
        """String representation"""
        return f"Quaternion({self.x}, {self.y}, {self.z}, {self.w})"
    
    def __add__(Quaternion self, Quaternion other):
        return Quaternion(
            self.x + other.x,
            self.y + other.y,
            self.z + other.z,
            self.w + other.w
        )
    
    def __sub__(Quaternion self, Quaternion other):
        return Quaternion(
            self.x - other.x,
            self.y - other.y,
            self.z - other.z,
            self.w - other.w
        )
    
    def __mul__(self, value):
        """
        Multiplication operator, handles:
        - Quaternion-scalar: scales each component
        - Quaternion-Quaternion: quaternion multiplication (composition of rotations)
        """
        # Quaternion-scalar multiplication
        # Here, we need to declare the type variables outside of conditional blocks
        cdef Quaternion q
        
        if isinstance(value, (int, float)):
            return Quaternion(
                self.x * value, 
                self.y * value, 
                self.z * value, 
                self.w * value
            )
        # Quaternion-quaternion multiplication (composition of rotations)
        elif isinstance(value, Quaternion):
            # We've already declared q above, so here we just assign to it
            q = <Quaternion>value
            
            # Hamilton product
            return Quaternion(
                self.w * q.x + self.x * q.w + self.y * q.z - self.z * q.y,
                self.w * q.y - self.x * q.z + self.y * q.w + self.z * q.x,
                self.w * q.z + self.x * q.y - self.y * q.x + self.z * q.w,
                self.w * q.w - self.x * q.x - self.y * q.y - self.z * q.z
            )
        else:
            return NotImplemented
    
    def __eq__(self, other):
        """Equality check"""
        if not isinstance(other, Quaternion):
            return False
        cdef Quaternion q = <Quaternion>other
        return (
            abs(self.x - q.x) < 1e-9 and 
            abs(self.y - q.y) < 1e-9 and 
            abs(self.z - q.z) < 1e-9 and 
            abs(self.w - q.w) < 1e-9
        )
    
    cpdef double length(self):
        """Get the length (magnitude) of the quaternion"""
        return sqrt(self.x * self.x + self.y * self.y + self.z * self.z + self.w * self.w)
    
    cpdef Quaternion normalize(self):
        """Return a normalized quaternion (unit quaternion)"""
        cdef double len_val = self.length()
        if len_val < 1e-10:
            return Quaternion(0, 0, 0, 1)  # Return identity if length is too close to zero
        
        return Quaternion(
            self.x / len_val,
            self.y / len_val,
            self.z / len_val,
            self.w / len_val
        )
    
    cpdef Quaternion conjugate(self):
        """Return the conjugate of this quaternion"""
        return Quaternion(-self.x, -self.y, -self.z, self.w)
    
    cpdef Quaternion inverse(self):
        """Return the inverse of this quaternion"""
        cdef double len_sq = (
            self.x * self.x + 
            self.y * self.y + 
            self.z * self.z + 
            self.w * self.w
        )
        
        if len_sq < 1e-10:
            return Quaternion(0, 0, 0, 1)  # Return identity if length squared is too small
        
        cdef double inv_len_sq = 1.0 / len_sq
        
        return Quaternion(
            -self.x * inv_len_sq,
            -self.y * inv_len_sq,
            -self.z * inv_len_sq,
             self.w * inv_len_sq
        )
    
    cpdef Vector3 rotate_vector3(self, Vector3 v):
        """Rotate a 3D vector using this quaternion"""
        # Pure quaternion from the vector
        cdef Quaternion vq = Quaternion(v.x, v.y, v.z, 0)
        
        # q * v * q^-1 (quaternion sandwich)
        cdef Quaternion q_inv = self.conjugate()  # For unit quaternions, conjugate == inverse
        cdef Quaternion result = self * vq * q_inv
        
        return Vector3(result.x, result.y, result.z)
    
    cpdef Matrix4 to_rotation_matrix(self):
        """Convert this quaternion to a rotation matrix"""
        cdef Matrix4 m = Matrix4()
        
        # Normalize the quaternion to ensure it represents a valid rotation
        cdef Quaternion q = self.normalize()
        
        cdef double xx = q.x * q.x
        cdef double xy = q.x * q.y
        cdef double xz = q.x * q.z
        cdef double xw = q.x * q.w
        
        cdef double yy = q.y * q.y
        cdef double yz = q.y * q.z
        cdef double yw = q.y * q.w
        
        cdef double zz = q.z * q.z
        cdef double zw = q.z * q.w
        
        # Row 0
        m.data[0] = 1 - 2 * (yy + zz)
        m.data[1] = 2 * (xy - zw)
        m.data[2] = 2 * (xz + yw)
        m.data[3] = 0
        
        # Row 1
        m.data[4] = 2 * (xy + zw)
        m.data[5] = 1 - 2 * (xx + zz)
        m.data[6] = 2 * (yz - xw)
        m.data[7] = 0
        
        # Row 2
        m.data[8] = 2 * (xz - yw)
        m.data[9] = 2 * (yz + xw)
        m.data[10] = 1 - 2 * (xx + yy)
        m.data[11] = 0
        
        # Row 3
        m.data[12] = 0
        m.data[13] = 0
        m.data[14] = 0
        m.data[15] = 1
        
        return m
    
    cpdef Quaternion copy(self):
        """Create a copy of this quaternion"""
        return Quaternion(self.x, self.y, self.z, self.w)
    
    @staticmethod
    cdef Quaternion identity():
        """Create an identity quaternion (no rotation)"""
        return Quaternion(0, 0, 0, 1)
    
    @staticmethod
    cdef Quaternion from_axis_angle(Vector3 axis, double angle):
        """Create a quaternion from an axis and an angle (radians)"""
        cdef Vector3 norm_axis = axis.normalize()
        cdef double half_angle = angle * 0.5
        cdef double sin_half = sin(half_angle)
        
        return Quaternion(
            norm_axis.x * sin_half,
            norm_axis.y * sin_half,
            norm_axis.z * sin_half,
            cos(half_angle)
        )
    
    @staticmethod
    cdef Quaternion from_euler_angles(double x, double y, double z):
        """Create a quaternion from Euler angles (radians)"""
        # Convert Euler angles to quaternion using the ZYX convention
        cdef double half_x = x * 0.5
        cdef double half_y = y * 0.5
        cdef double half_z = z * 0.5
        
        cdef double cx = cos(half_x)
        cdef double sx = sin(half_x)
        cdef double cy = cos(half_y)
        cdef double sy = sin(half_y)
        cdef double cz = cos(half_z)
        cdef double sz = sin(half_z)
        
        # ZYX convention
        return Quaternion(
            cx * cy * sz - sx * sy * cz,
            cx * sy * cz + sx * cy * sz,
            sx * cy * cz - cx * sy * sz,
            cx * cy * cz + sx * sy * sz
        )
    
    @staticmethod
    cdef Quaternion from_matrix(Matrix4 m):
        """Create a quaternion from a rotation matrix"""
        cdef double trace = m.data[0] + m.data[5] + m.data[10]
        cdef double x, y, z, w, s
        
        if trace > 0:
            # Trace is positive
            s = 0.5 / sqrt(trace + 1.0)
            w = 0.25 / s
            x = (m.data[9] - m.data[6]) * s
            y = (m.data[2] - m.data[8]) * s
            z = (m.data[4] - m.data[1]) * s
        elif m.data[0] > m.data[5] and m.data[0] > m.data[10]:
            # Element [0][0] is largest
            s = 2.0 * sqrt(1.0 + m.data[0] - m.data[5] - m.data[10])
            w = (m.data[9] - m.data[6]) / s
            x = 0.25 * s
            y = (m.data[1] + m.data[4]) / s
            z = (m.data[2] + m.data[8]) / s
        elif m.data[5] > m.data[10]:
            # Element [1][1] is largest
            s = 2.0 * sqrt(1.0 + m.data[5] - m.data[0] - m.data[10])
            w = (m.data[2] - m.data[8]) / s
            x = (m.data[1] + m.data[4]) / s
            y = 0.25 * s
            z = (m.data[6] + m.data[9]) / s
        else:
            # Element [2][2] is largest
            s = 2.0 * sqrt(1.0 + m.data[10] - m.data[0] - m.data[5])
            w = (m.data[4] - m.data[1]) / s
            x = (m.data[2] + m.data[8]) / s
            y = (m.data[6] + m.data[9]) / s
            z = 0.25 * s
        
        return Quaternion(x, y, z, w)
    
    @staticmethod
    cdef Quaternion slerp(Quaternion a, Quaternion b, double t):
        """Spherical linear interpolation between two quaternions"""
        # Clamp t to range [0, 1]
        t = max(0.0, min(t, 1.0))
        
        # Make sure we take the shortest path
        cdef double dot = a.x * b.x + a.y * b.y + a.z * b.z + a.w * b.w
        cdef Quaternion b_adj = Quaternion(b.x, b.y, b.z, b.w)
        
        # If dot product is negative, negate one quaternion to take shortest path
        if dot < 0:
            b_adj.x = -b.x
            b_adj.y = -b.y
            b_adj.z = -b.z
            b_adj.w = -b.w
            dot = -dot
        
        # Clamp dot product to valid domain of acos
        dot = max(-1.0, min(dot, 1.0))
        
        cdef double theta = acos(dot)
        cdef double sin_theta = sin(theta)
        
        # If angle is very small, do linear interpolation
        if sin_theta < 1e-6:
            return Quaternion(
                a.x * (1.0 - t) + b_adj.x * t,
                a.y * (1.0 - t) + b_adj.y * t,
                a.z * (1.0 - t) + b_adj.z * t,
                a.w * (1.0 - t) + b_adj.w * t
            ).normalize()
        
        # Calculate slerp coefficients
        cdef double s0 = sin((1.0 - t) * theta) / sin_theta
        cdef double s1 = sin(t * theta) / sin_theta
        
        return Quaternion(
            a.x * s0 + b_adj.x * s1,
            a.y * s0 + b_adj.y * s1,
            a.z * s0 + b_adj.z * s1,
            a.w * s0 + b_adj.w * s1
        ).normalize()
