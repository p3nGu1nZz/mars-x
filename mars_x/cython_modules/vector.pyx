# cython: language_level=3
# cython: boundscheck=False
# cython: wraparound=False

import cython
from libc.math cimport sqrt

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
    
    def __mul__(self, value):
        if isinstance(value, (int, float)):
            return Vector2(self.x * value, self.y * value)
        elif isinstance(value, Vector2):
            return Vector2(self.x * (<Vector2>value).x, self.y * (<Vector2>value).y)
        else:
            return NotImplemented
    
    def __truediv__(self, value):
        if isinstance(value, (int, float)):
            return Vector2(self.x / value, self.y / value)
        elif isinstance(value, Vector2):
            return Vector2(self.x / (<Vector2>value).x, self.y / (<Vector2>value).y)
        else:
            return NotImplemented
    
    cpdef double length(self):
        return sqrt(self.x * self.x + self.y * self.y)
    
    cpdef Vector2 normalize(self):
        cdef double len_val = self.length()
        if len_val > 0:
            return Vector2(self.x / len_val, self.y / len_val)
        return Vector2(0, 0)
    
    cpdef double dot(self, Vector2 other):
        return self.x * other.x + self.y * other.y
    
    cpdef Vector2 copy(self):
        return Vector2(self.x, self.y)
    
    @staticmethod
    def distance(Vector2 a, Vector2 b):
        cdef double dx = b.x - a.x
        cdef double dy = b.y - a.y
        return sqrt(dx * dx + dy * dy)


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
            return Vector3(self.x / value, self.y / value, self.z / value)
        elif isinstance(value, Vector3):
            return Vector3(self.x / (<Vector3>value).x, 
                         self.y / (<Vector3>value).y, 
                         self.z / (<Vector3>value).z)
        else:
            return NotImplemented
    
    cpdef double length(self):
        return sqrt(self.x * self.x + self.y * self.y + self.z * self.z)
    
    cpdef Vector3 normalize(self):
        cdef double len_val = self.length()
        if len_val > 0:
            return Vector3(self.x / len_val, self.y / len_val, self.z / len_val)
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
    
    @staticmethod
    def distance(Vector3 a, Vector3 b):
        cdef double dx = b.x - a.x
        cdef double dy = b.y - a.y
        cdef double dz = b.z - a.z
        return sqrt(dx * dx + dy * dy + dz * dz)


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
            return Vector4(self.x / value, self.y / value, 
                         self.z / value, self.w / value)
        elif isinstance(value, Vector4):
            return Vector4(self.x / (<Vector4>value).x, 
                         self.y / (<Vector4>value).y,
                         self.z / (<Vector4>value).z,
                         self.w / (<Vector4>value).w)
        else:
            return NotImplemented
    
    cpdef double length(self):
        return sqrt(self.x * self.x + self.y * self.y + 
                   self.z * self.z + self.w * self.w)
    
    cpdef Vector4 normalize(self):
        cdef double len_val = self.length()
        if len_val > 0:
            return Vector4(self.x / len_val, self.y / len_val, 
                         self.z / len_val, self.w / len_val)
        return Vector4(0, 0, 0, 0)
    
    cpdef double dot(self, Vector4 other):
        return (self.x * other.x + self.y * other.y + 
                self.z * other.z + self.w * other.w)
    
    cpdef Vector4 copy(self):
        return Vector4(self.x, self.y, self.z, self.w)
    
    @staticmethod
    def distance(Vector4 a, Vector4 b):
        cdef double dx = b.x - a.x
        cdef double dy = b.y - a.y
        cdef double dz = b.z - a.z
        cdef double dw = b.w - a.w
        return sqrt(dx * dx + dy * dy + dz * dz + dw * dw)
    
    # Convert to Vector3 (perspective division)
    def to_vector3(self):
        if self.w != 0:
            return Vector3(self.x / self.w, self.y / self.w, self.z / self.w)
        return Vector3(self.x, self.y, self.z)
