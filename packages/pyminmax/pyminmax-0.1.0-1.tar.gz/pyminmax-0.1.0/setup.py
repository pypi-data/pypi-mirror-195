# from distutils.core import setup, Extension

# module = Extension('pyminmax.minmax', sources=["src/pyminmax/minmaxmodule.c"])

# setup(ext_modules=[module])

from setuptools import setup, Extension

module = Extension('pyminmax.minmax', sources=["src/pyminmax/minmaxmodule.c"])

setup(ext_modules=[module])
