# cython: language_level=3

# Fast math functions - simplified exception handling
cdef double fast_invsqrt(double x) nogil
cdef double fast_sqrt(double x) nogil
cdef double fast_sin(double x) nogil
cdef double fast_cos(double x) nogil

# Define Vector structs - renamed to Vec to avoid conflicts with classes
cdef struct Vec2:
    double x
    double y

cdef struct Vec3:
    double x
    double y
    double z

cdef struct Vec4:
    double x
    double y
    double z
    double w

# Function declarations for Vec2
cdef Vec2 vec2_create(double x, double y)
cdef Vec2 vec2_add(Vec2 a, Vec2 b)
cdef Vec2 vec2_sub(Vec2 a, Vec2 b)
cdef Vec2 vec2_mul(Vec2 v, double scalar)
cdef Vec2 vec2_div(Vec2 v, double scalar)
cdef Vec2 vec2_copy(Vec2 v)
cdef double vec2_length_squared(Vec2 v)
cdef Vec2 vec2_normalize(Vec2 v)
cdef double vec2_dot(Vec2 a, Vec2 b)
cdef double vec2_cross(Vec2 a, Vec2 b)
cdef double vec2_angle(Vec2 v)
cdef Vec2 vec2_rotate(Vec2 v, double angle)
cdef bint vec2_is_zero(Vec2 v)
cdef bint vec2_approx_equal(Vec2 a, Vec2 b, double epsilon)

# Function declarations for Vec3
cdef Vec3 vec3_create(double x, double y, double z)
cdef Vec3 vec3_add(Vec3 a, Vec3 b)
cdef Vec3 vec3_sub(Vec3 a, Vec3 b)
cdef Vec3 vec3_mul(Vec3 v, double scalar)
cdef Vec3 vec3_div(Vec3 v, double scalar)
cdef double vec3_length_squared(Vec3 v)
cdef Vec3 vec3_normalize(Vec3 v)
cdef double vec3_dot(Vec3 a, Vec3 b)
cdef Vec3 vec3_cross(Vec3 a, Vec3 b)
cdef Vec3 vec3_copy(Vec3 v)

# Function declarations for Vec4
cdef Vec4 vec4_create(double x, double y, double z, double w)
cdef Vec4 vec4_add(Vec4 a, Vec4 b)
cdef Vec4 vec4_sub(Vec4 a, Vec4 b)
cdef Vec4 vec4_mul(Vec4 v, double scalar)
cdef Vec4 vec4_div(Vec4 v, double scalar)
cdef double vec4_length_squared(Vec4 v)
cdef Vec4 vec4_normalize(Vec4 v)  # Changed from vec4_normalize_approx
cdef double vec4_dot(Vec4 a, Vec4 b)
cdef Vec4 vec4_copy(Vec4 v)
cdef Vec3 vec4_to_vec3(Vec4 v)

# Classes for Python API
cdef class Vector2:
    cdef public double x
    cdef public double y
    
    cpdef Vector2 copy(self)
    cpdef double length_squared(self)
    cpdef double magnitude(self)
    cpdef Vector2 normalize(self)
    cpdef double dot(self, Vector2 other)
    cpdef double cross(self, Vector2 other)
    cpdef double angle(self)
    cpdef double angle_to(self, Vector2 other)
    cpdef Vector2 rotate(self, double angle)
    cpdef bint is_zero(self)

cdef class Vector3:
    cdef public double x
    cdef public double y
    cdef public double z
    
    cpdef double length_squared(self)
    cpdef double magnitude(self)
    cpdef Vector3 normalize(self)
    cpdef double dot(self, Vector3 other)
    cpdef Vector3 cross(self, Vector3 other)
    cpdef Vector3 copy(self)

cdef class Vector4:
    cdef public double x
    cdef public double y
    cdef public double z
    cdef public double w
    
    cpdef double length_squared(self)
    cpdef double magnitude(self)
    cpdef Vector4 normalize(self)
    cpdef double dot(self, Vector4 other)
    cpdef Vector4 copy(self)
