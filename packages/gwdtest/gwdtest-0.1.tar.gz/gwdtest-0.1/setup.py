from distutils.core import  setup
import setuptools
packages = ['gwdtest']
setup(  name = "gwdtest",
        version = "0.1",
        description = "Test package for gwd",
        author="GWD",
        packages=packages,
        packages_dir={'requests': 'requests'},
        )
