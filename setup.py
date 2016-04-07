#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from setuptools import setup, find_packages

setup(name='HWToolkit',
      version='0.1',
      description='hdl synthesis toolkit',
      url='https://github.com/Nic30/HWToolkit',
      author='Michal Orsak',
      author_email='michal.o.socials@gmail.com',
      install_requires=[
        'myhdl',
        'Pillow',    # altium scheme reader
        'sympy',  # symbolic math
        'simpy',  # discrete simulator 
        'jinja2', # hdl templates renderer, visualizer renderer
        'flask',  # visualizer
        'multiprocess', # used instead of multiprocessing (can serialize functions) in parser
      ],
      license='MIT',
      packages = find_packages(),
      package_data={'vhdl_toolkit': ['*.vhd', '*.jar'],
                    'visualizer' : ['*.html', '*.js', '*.css', '*.ico', 
                                    '*.png', '*.oft', '*.eot', '*.svg', 
                                    '*.ttf', '*.woff']},
      include_package_data=True,
      zip_safe=False)
