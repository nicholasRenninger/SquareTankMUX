from distutils.core import setup
import py2exe # line is needed for creating executable

filename = raw_input('Enter the desired filename: ')
print(filename)
setup(console=[filename])
