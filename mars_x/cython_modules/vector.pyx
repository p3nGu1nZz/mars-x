# cython: language_level=3
# cython: boundscheck=False
# cython: wraparound=False

import cython
cimport libc.math  # type: ignore
from libc.math cimport sin, cos, atan2, M_PI, acos, sqrt  # type: ignore

# Fast inverse square root approximation (Quake algorithm variant)
@cython.cdivision(True)
cdef double fast_invsqrt(double x):
    """Fast inverse square root approximation."""
    if x <= 0:
        return 0.0
    
    # Instead of binary reinterpretation trick, use Newton's method
    # for quick approximation (more portable in Cython)
    cdef double y = 1.0 / sqrt(x)  # Initial approximation
    
    # One Newton iteration for refinement: y = y * (1.5 - 0.5 * x * y * y)
    y = y * (1.5 - 0.5 * x * y * y)
    
    return y

# Vec2 functions
cdef Vec2 vec2_create(double x, double y):
    cdef Vec2 v
    v.x = x
    v.y = y
    return v

cdef Vec2 vec2_add(Vec2 a, Vec2 b):
    cdef Vec2 result
    result.x = a.x + b.x
    result.y = a.y + b.y
    return result

cdef Vec2 vec2_sub(Vec2 a, Vec2 b):
    cdef Vec2 result
    result.x = a.x - b.x
    result.y = a.y - b.y
    return result

cdef Vec2 vec2_mul(Vec2 v, double scalar):
    cdef Vec2 result
    result.x = v.x * scalar
    result.y = v.y * scalar
    return result

@cython.cdivision(True)
cdef Vec2 vec2_div(Vec2 v, double scalar):
    cdef Vec2 result
    if scalar == 0:
        result.x = 0
        result.y = 0
    else:
        result.x = v.x / scalar
        result.y = v.y / scalar
    return result

cdef Vec2 vec2_copy(Vec2 v):
    cdef Vec2 result
    result.x = v.x
    result.y = v.y
    return result

cdef double vec2_length_squared(Vec2 v):
    return v.x * v.x + v.y * v.y

cdef Vec2 vec2_normalize(Vec2 v):
    """
    Normalize a vector to unit length using fast inverse square root.
    """
    cdef double len_sq = v.x * v.x + v.y * v.y
    cdef Vec2 result
    cdef double inv_len  # Move declaration to the beginning of function
    
    if len_sq > 1e-10:  # Avoid division by near-zero
        inv_len = fast_invsqrt(len_sq)  # Now just assignment
        result.x = v.x * inv_len
        result.y = v.y * inv_len
    else:
        result.x = 0
        result.y = 0
    
    return result

cdef double vec2_dot(Vec2 a, Vec2 b):
    return a.x * b.x + a.y * b.y

cdef double vec2_cross(Vec2 a, Vec2 b):
    return a.x * b.y - a.y * b.x

cdef double vec2_angle(Vec2 v):
    return atan2(v.y, v.x)

cdef Vec2 vec2_rotate(Vec2 v, double angle):
    cdef Vec2 result
    cdef double cs = cos(angle)
    cdef double sn = sin(angle)
    result.x = v.x * cs - v.y * sn
    result.y = v.x * sn + v.y * cs
    return result

cdef bint vec2_is_zero(Vec2 v):
    return (v.x * v.x + v.y * v.y) < 1e-10

cdef bint vec2_approx_equal(Vec2 a, Vec2 b, double epsilon):
    cdef double dx = a.x - b.x
    cdef double dy = a.y - b.y
    return (dx * dx + dy * dy) < epsilon * epsilon

# Vector3 functions with Vec3 structs
cdef Vec3 vec3_create(double x, double y, double z):
    cdef Vec3 v
    v.x = x
    v.y = y
    v.z = z
    return v

cdef Vec3 vec3_add(Vec3 a, Vec3 b):
    cdef Vec3 result
    result.x = a.x + b.x
    result.y = a.y + b.y
    result.z = a.z + b.z
    return result

cdef Vec3 vec3_sub(Vec3 a, Vec3 b):
    cdef Vec3 result
    result.x = a.x - b.x
    result.y = a.y - b.y
    result.z = a.z - b.z
    return result

cdef Vec3 vec3_mul(Vec3 v, double scalar):
    cdef Vec3 result
    result.x = v.x * scalar
    result.y = v.y * scalar
    result.z = v.z * scalar
    return result

@cython.cdivision(True)
cdef Vec3 vec3_div(Vec3 v, double scalar):
    cdef Vec3 result
    if scalar == 0:
        result.x = 0
        result.y = 0
        result.z = 0
    else:
        result.x = v.x / scalar
        result.y = v.y / scalar
        result.z = v.z / scalar
    return result

cdef double vec3_length_squared(Vec3 v):
    return v.x * v.x + v.y * v.y + v.z * v.z

cdef Vec3 vec3_normalize(Vec3 v):
    """
    Normalize a vector to unit length using fast inverse square root.
    """
    cdef double len_sq = v.x * v.x + v.y * v.y + v.z * v.z
    cdef Vec3 result
    cdef double inv_len  # Move declaration to the beginning of function
    
    if len_sq > 1e-10:
        inv_len = fast_invsqrt(len_sq)  # Now just assignment
        result.x = v.x * inv_len
        result.y = v.y * inv_len
        result.z = v.z * inv_len
    else:
        result.x = 0
        result.y = 0
        result.z = 0
    return result

cdef double vec3_dot(Vec3 a, Vec3 b):
    return a.x * b.x + a.y * b.y + a.z * b.z

cdef Vec3 vec3_cross(Vec3 a, Vec3 b):
    cdef Vec3 result
    result.x = a.y * b.z - a.z * b.y
    result.y = a.z * b.x - a.x * b.z
    result.z = a.x * b.y - a.y * b.x
    return result

cdef Vec3 vec3_copy(Vec3 v):
    cdef Vec3 result
    result.x = v.x
    result.y = v.y
    result.z = v.z
    return result

# Vec4 functions
cdef Vec4 vec4_create(double x, double y, double z, double w):
    cdef Vec4 v
    v.x = x
    v.y = y
    v.z = z
    v.w = w
    return v

cdef Vec4 vec4_add(Vec4 a, Vec4 b):
    cdef Vec4 result
    result.x = a.x + b.x
    result.y = a.y + b.y
    result.z = a.z + b.z
    result.w = a.w + b.w
    return result

cdef Vec4 vec4_sub(Vec4 a, Vec4 b):
    cdef Vec4 result
    result.x = a.x - b.x
    result.y = a.y - b.y
    result.z = a.z - b.z
    result.w = a.w - b.w
    return result

cdef Vec4 vec4_mul(Vec4 v, double scalar):
    cdef Vec4 result
    result.x = v.x * scalar
    result.y = v.y * scalar
    result.z = v.z * scalar
    result.w = v.w * scalar
    return result

@cython.cdivision(True)
cdef Vec4 vec4_div(Vec4 v, double scalar):
    cdef Vec4 result
    if scalar == 0:
        result.x = 0
        result.y = 0
        result.z = 0
        result.w = 0
    else:
        result.x = v.x / scalar
        result.y = v.y / scalar
        result.z = v.z / scalar
        result.w = v.w / scalar
    return result

cdef double vec4_length_squared(Vec4 v):
    return v.x * v.x + v.y * v.y + v.z * v.z + v.w * v.w

cdef Vec4 vec4_normalize(Vec4 v):
    """
    Normalize a vector to unit length using fast inverse square root.
    """
    cdef double len_sq = v.x * v.x + v.y * v.y + v.z * v.z + v.w * v.w
    cdef Vec4 result
    cdef double inv_len  # Move declaration to the beginning of function
    
    if len_sq > 1e-10:
        inv_len = fast_invsqrt(len_sq)  # Now just assignment
        result.x = v.x * inv_len
        result.y = v.y * inv_len
        result.z = v.z * inv_len
        result.w = v.w * inv_len
    else:
        result.x = 0
        result.y = 0
        result.z = 0
        result.w = 0
    return result

cdef double vec4_dot(Vec4 a, Vec4 b):
    return a.x * b.x + a.y * b.y + a.z * b.z + a.w * b.w

cdef Vec4 vec4_copy(Vec4 v):
    cdef Vec4 result
    result.x = v.x
    result.y = v.y
    result.z = v.z
    result.w = v.w
    return result

@cython.cdivision(True)
cdef Vec3 vec4_to_vec3(Vec4 v):
    cdef Vec3 result
    if v.w != 0:
        result.x = v.x / v.w
        result.y = v.y / v.w
        result.z = v.z / v.w
    else:
        result.x = v.x
        result.y = v.y
        result.z = v.z
    return result

# Class implementations
cdef class Vector2:
    def __init__(self, double x=0.0, double y=0.0):
        self.x = x
        self.y = y
    
    def __repr__(self):
        return f"Vector2({self.x}, {self.y})"
    
    def __add__(Vector2 self, Vector2 other):
        return Vector2(self.x + other.x, self.y + other.y)
    
    def __sub__(Vector2 self, Vector2 other):
        return Vector2(self.x - other.x, self.y - other.y)
    
    def __mul__(Vector2 self, double scalar):
        return Vector2(self.x * scalar, self.y * scalar)
    
    def __truediv__(Vector2 self, double scalar):
        if scalar == 0:
            raise ZeroDivisionError("Division by zero")
        return Vector2(self.x / scalar, self.y / scalar)
    
    def __neg__(self):
        return Vector2(-self.x, -self.y)
    
    cpdef Vector2 copy(self):
        return Vector2(self.x, self.y)
    
    cpdef double length_squared(self):
        """Return squared length of vector (faster than magnitude)"""
        return self.x * self.x + self.y * self.y
    
    cpdef double magnitude(self):
        """Return magnitude (length) of the vector using fast approximation"""
        cdef double len_sq = self.length_squared()
        if len_sq == 0:
            return 0
        return len_sq * fast_invsqrt(len_sq)
    
    cpdef Vector2 normalize(self):
        """Return normalized vector using fast approximation"""
        cdef double len_sq = self.length_squared()
        cdef double inv_len  # Move declaration to the beginning of function
        
        if len_sq > 1e-10:
            inv_len = fast_invsqrt(len_sq)
            return Vector2(self.x * inv_len, self.y * inv_len)
        return Vector2(0, 0)
    
    cpdef double dot(self, Vector2 other):
        return self.x * other.x + self.y * other.y
    
    cpdef double cross(self, Vector2 other):
        return self.x * other.y - self.y * other.x
    
    cpdef double angle(self):
        # Returns angle in radians
        return atan2(self.y, self.x)
    
    cpdef double angle_to(self, Vector2 other):
        # Use dot product for cosine of angle, avoiding sqrt
        cdef double dot_product = self.dot(other)
        cdef double len1_sq = self.length_squared()
        cdef double len2_sq = other.length_squared()
        cdef double cos_angle 
        cdef double cross_product
        
        if len1_sq == 0 or len2_sq == 0:
            return 0
        
        # Compute cosine using scaled dot product
        cos_angle = dot_product * fast_invsqrt(len1_sq) * fast_invsqrt(len2_sq)
        
        # Clamp to avoid numerical errors
        if cos_angle > 1.0:
            cos_angle = 1.0
        elif cos_angle < -1.0:
            cos_angle = -1.0
        
        # Use cross product to determine the direction
        cross_product = self.cross(other)
        if cross_product < 0:
            return -acos(cos_angle)
        else:
            return acos(cos_angle)
    
    cpdef Vector2 rotate(self, double angle):
        # Rotates the vector by angle (in radians)
        cdef double cs = cos(angle)
        cdef double sn = sin(angle)
        return Vector2(
            self.x * cs - self.y * sn,
            self.x * sn + self.y * cs
        )
    
    cpdef bint is_zero(self):
        """Check if vector is approximately zero"""
        return self.length_squared() < 1e-10

cdef class Vector3:
    def __init__(self, double x=0.0, double y=0.0, double z=0.0):
        self.x = x
        self.y = y
        self.z = z
    
    def __repr__(self):
        return f"Vector3({self.x}, {self.y}, {self.z})"
    
    def __add__(Vector3 self, Vector3 other):
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __sub__(Vector3 self, Vector3 other):
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)
    
    def __mul__(self, value):
        if isinstance(value, (int, float)):
            return Vector3(self.x * value, self.y * value, self.z * value)
        elif isinstance(value, Vector3):
            return Vector3(self.x * (<Vector3>value).x, 
                           self.y * (<Vector3>value).y, 
                           self.z * (<Vector3>value).z)
        else:
            return NotImplemented
    
    def __truediv__(self, value):
        if isinstance(value, (int, float)):
            if value == 0:
                raise ZeroDivisionError("Division by zero")
            return Vector3(self.x / value, self.y / value, self.z / value)
        elif isinstance(value, Vector3):
            return Vector3(
                self.x / (<Vector3>value).x if (<Vector3>value).x != 0 else 0, 
                self.y / (<Vector3>value).y if (<Vector3>value).y != 0 else 0,
                self.z / (<Vector3>value).z if (<Vector3>value).z != 0 else 0
            )
        else:
            return NotImplemented
    
    cpdef double length_squared(self):
        """Return squared length of vector (faster than magnitude)"""
        return self.x * self.x + self.y * self.y + self.z * self.z
    
    cpdef double magnitude(self):
        """Return magnitude (length) of the vector using fast approximation"""
        cdef double len_sq = self.length_squared()
        if len_sq == 0:
            return 0
        return len_sq * fast_invsqrt(len_sq)
    
    cpdef Vector3 normalize(self):
        """Return normalized vector using fast approximation"""
        cdef double len_sq = self.length_squared()
        cdef double inv_len  # Move declaration to the beginning of function
        
        if len_sq > 1e-10:
            inv_len = fast_invsqrt(len_sq)
            return Vector3(self.x * inv_len, self.y * inv_len, self.z * inv_len)
        return Vector3(0, 0, 0)
    
    cpdef double dot(self, Vector3 other):
        return self.x * other.x + self.y * other.y + self.z * other.z
    
    cpdef Vector3 cross(self, Vector3 other):
        return Vector3(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x
        )
    
    cpdef Vector3 copy(self):
        return Vector3(self.x, self.y, self.z)

cdef class Vector4:
    def __init__(self, double x=0.0, double y=0.0, double z=0.0, double w=1.0):
        self.x = x
        self.y = y
        self.z = z
        self.w = w
    
    def __repr__(self):
        return f"Vector4({self.x}, {self.y}, {self.z}, {self.w})"
    
    def __add__(Vector4 self, Vector4 other):
        return Vector4(self.x + other.x, self.y + other.y, 
                     self.z + other.z, self.w + other.w)
    
    def __sub__(Vector4 self, Vector4 other):
        return Vector4(self.x - other.x, self.y - other.y, 
                     self.z - other.z, self.w - other.w)
    
    def __mul__(self, value):
        if isinstance(value, (int, float)):
            return Vector4(self.x * value, self.y * value, 
                         self.z * value, self.w * value)
        elif isinstance(value, Vector4):
            return Vector4(self.x * (<Vector4>value).x, 
                         self.y * (<Vector4>value).y,
                         self.z * (<Vector4>value).z,
                         self.w * (<Vector4>value).w)
        else:
            return NotImplemented
    
    def __truediv__(self, value):
        if isinstance(value, (int, float)):
            if value == 0:
                raise ZeroDivisionError("Division by zero")
            return Vector4(self.x / value, self.y / value, 
                         self.z / value, self.w / value)
        elif isinstance(value, Vector4):
            return Vector4(
                self.x / (<Vector4>value).x if (<Vector4>value).x != 0 else 0,
                self.y / (<Vector4>value).y if (<Vector4>value).y != 0 else 0,
                self.z / (<Vector4>value).z if (<Vector4>value).z != 0 else 0,
                self.w / (<Vector4>value).w if (<Vector4>value).w != 0 else 0
            )
        else:
            return NotImplemented
    
    cpdef double length_squared(self):
        """Return squared length of vector (faster than magnitude)"""
        return self.x * self.x + self.y * self.y + self.z * self.z + self.w * self.w
    
    cpdef double magnitude(self):
        """Return magnitude (length) of the vector using fast approximation"""
        cdef double len_sq = self.length_squared()
        if len_sq == 0:
            return 0
        return len_sq * fast_invsqrt(len_sq)
    
    cpdef Vector4 normalize(self):
        """Return normalized vector using fast approximation"""
        cdef double len_sq = self.length_squared()
        cdef double inv_len  # Move declaration to the beginning of function
        
        if len_sq > 1e-10:
            inv_len = fast_invsqrt(len_sq)
            return Vector4(self.x * inv_len, self.y * inv_len, 
                         self.z * inv_len, self.w * inv_len)
        return Vector4(0, 0, 0, 0)
    
    cpdef double dot(self, Vector4 other):
        return (self.x * other.x + self.y * other.y + 
                self.z * other.z + self.w * other.w)
    
    cpdef Vector4 copy(self):
        return Vector4(self.x, self.y, self.z, self.w)
    
    # Convert to Vector3 (perspective division)
    def to_vector3(self):
        if self.w != 0:
            return Vector3(self.x / self.w, self.y / self.w, self.z / self.w)
        return Vector3(self.x, self.y, self.z)
