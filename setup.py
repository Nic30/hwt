#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from os import path
from setuptools import setup, find_packages

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(name="hwt",
      version="2.6",
      description="hdl synthesis toolkit",
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/Nic30/hwt",
      author="Michal Orsak",
      author_email="michal.o.socials@gmail.com",
      classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Scientific/Engineering :: Electronic Design Automation (EDA)",
        "Topic :: System :: Hardware",
        "Topic :: System :: Emulators",
        "Topic :: Utilities"],
      install_requires=[
          "jinja2",  # template engine
          "pyDigitalWaveTools>=0.3",  # simulator output dumping
          "ipCorePackager"
      ],
      license="MIT",
      packages=find_packages(),
      package_data={"hwt": ["*.vhd", "*.v",
                            "*.py.template",
                            "*.cpp.template"]},
      include_package_data=True,
      zip_safe=False)
