#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from setuptools import setup, find_packages

setup(name='hwtoolkit',
      version='0.2',
      description='hdl synthesis toolkit',
      url='https://github.com/Nic30/HWToolkit',
      author='Michal Orsak',
      author_email='michal.o.socials@gmail.com',
      install_requires=[
        'myhdl',  # optional hls synthesizer (but used in some samples)
        'Pillow', # altium scheme reader
        'simpy',  # discrete simulator 
        'jinja2', # hdl templates renderer, visualizer renderer
        'flask'  # visualizer
      ],
      license='MIT',
      packages = find_packages(),
      package_data={'hwt': ['*.vhd', '*.v'],
                    'visualizer' : ['*.html', '*.js', '*.css', '*.ico', 
                                    '*.png', '*.oft', '*.eot', '*.svg', 
                                    '*.ttf', '*.woff']},
      include_package_data=True,
      zip_safe=False)
