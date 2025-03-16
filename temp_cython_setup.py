
import os
import sys
from setuptools import setup, Extension
from Cython.Build import cythonize

extensions = [
    Extension("mars_x.cython_modules.vector", ["mars_x/cython_modules/vector.pyx"]),
    Extension("mars_x.cython_modules.collision", ["mars_x/cython_modules/collision.pyx"]),
    Extension("mars_x.cython_modules.rigidbody", ["mars_x/cython_modules/rigidbody.pyx"]),
    Extension("mars_x.cython_modules.matrix", ["mars_x/cython_modules/matrix.pyx"]),
    Extension("mars_x.cython_modules.quaternion", ["mars_x/cython_modules/quaternion.pyx"])
]

setup(
    name="mars_x_cython_modules",
    ext_modules=cythonize(
        extensions,
        compiler_directives={
            'language_level': 3,
            'boundscheck': False,
            'wraparound': False
        }
    ),
)
