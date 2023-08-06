from setuptools import setup, Extension
import sys, os

version = '0.1.1'

setup(name='ImageExtras',
      version=version,
      description="Image Processing extra functions",
      long_description="""\
            Utilities and compiled algorithms to make Image Processing easier""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='image img dither luma',
      author='Adrià Brú i Cortés',
      author_email='adriabrucortes@gmail.com',
      url='',
      license='GPL3',
      packages=['imageextras', 'imageextras.src', 'imageextras.compiled'],
      package_data={'imageextras.compiled': ['dithering.cpython-310-x86_64-linux-gnu.so']},
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          'numpy'
      ],
      )
