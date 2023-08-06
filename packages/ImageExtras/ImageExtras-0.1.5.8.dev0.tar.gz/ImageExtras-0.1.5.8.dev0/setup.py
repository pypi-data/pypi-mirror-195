from setuptools import setup, Extension, find_packages
import sys, os

version = '0.1.5.8'

setup(name='ImageExtras',
      version=version,
      description="Image Processing extra functions",
      long_description="""\
            Utilities and compiled algorithms to make Image Processing easier""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='image img dither luma',
      author='Adrià Brú i Cortés',
      author_email='adriabrucortes@gmail.com',
      url='https://gitlab.com/adriabrucortes/imageextras',
      license='GPL3',
      packages = find_packages(), # get all directories with __init__.py in it
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          'numpy'
      ],
      requires_python = ">=3.9, <3.11"
      )
