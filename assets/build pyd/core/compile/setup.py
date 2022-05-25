from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
ext_modules = [
    Extension("core",  ["core.py"]),
]

setup(
    name = 'core',
    cmdclass = {'build_ext': build_ext},
    ext_modules = ext_modules
)
