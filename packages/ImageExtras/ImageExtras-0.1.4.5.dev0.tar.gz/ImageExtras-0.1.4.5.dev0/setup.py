from setuptools import setup, Extension
import sys, os

version = '0.1.4.5'

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
      packages=['imageextras',
                  'imageextras.src',
                  'imageextras.compiled',
                        'imageextras.compiled.dithering'],
      package_data={'imageextras.compiled.dithering': ['dithering.cpython-310-x86_64-linux-gnu.so',
                                                       'dithering.cp39-win_amd64.pyd']},
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          'numpy'
      ],
      )
