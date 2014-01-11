from distutils.core import setup, Extension
module1 = Extension('miya',sources = ['miyamodule.c'])
setup (name = 'miya package',version = '1.0',description = 'This is a miya package',ext_modules = [module1])