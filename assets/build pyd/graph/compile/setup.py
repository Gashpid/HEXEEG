from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
ext_modules = [
    Extension("graph",  ["graph.py"]),
]

setup(
    name = 'graph',
    cmdclass = {'build_ext': build_ext},
    ext_modules = ext_modules
)
