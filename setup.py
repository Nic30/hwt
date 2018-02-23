#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from setuptools import setup, find_packages


setup(name='hwt',
      version='2.1',
      description='hdl synthesis toolkit',
      url='https://github.com/Nic30/HWToolkit',
      author='Michal Orsak',
      author_email='michal.o.socials@gmail.com',
      install_requires=[
          'jinja2',  # templating engine
      ],
      license='MIT',
      packages=find_packages(),
      package_data={'hwt': ['*.vhd', '*.v',
                            '*.py.template',
                            '*.cpp.template']},
      include_package_data=True,
      zip_safe=False)
