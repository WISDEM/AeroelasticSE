from numpy.distutils.core import setup, Extension

setup (name = 'Rainflow',
        version = '1.0',
        description = 'This is a rainflow counter for fatigue loads on wind turbines',
        ext_modules = [Extension('_rainflow_swig', ['rainflow_swig_wrap.c', 'rainflow_swig.c'], extra_compile_args=['-O2'])])