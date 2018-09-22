# HWToolkit (hwt),
# the library for hardware development in Python
[![Build Status](https://travis-ci.org/Nic30/hwt.svg?branch=master)](https://travis-ci.org/Nic30/hwt)
[![Coverage Status](https://coveralls.io/repos/github/Nic30/hwt/badge.svg?branch=master)](https://coveralls.io/github/Nic30/hwt?branch=master)
[![PyPI version](https://badge.fury.io/py/hwt.svg)](http://badge.fury.io/py/hwt) 
[![Documentation Status](https://readthedocs.org/projects/hwtoolkit/badge/?version=latest)](http://hwtoolkit.readthedocs.io/en/latest/?badge=latest) 
[![Python version](https://img.shields.io/pypi/pyversions/hwt.svg)](https://img.shields.io/pypi/pyversions/hwt.svg)

## The goals of HWT

* Meta programing + HLS, standard code generators to prevent code duplications.
* Integration with community and commercial tools, flexible lightway user extensible architecture.
* Simple verifications and testing.

## Features

* Meta Hardware Description Language (example [simple](https://github.com/Nic30/hwtLib/blob/master/hwtLib/samples/simple.py), [showcase](https://github.com/Nic30/hwtLib/blob/master/hwtLib/samples/showcase0.py)). It is somewhere between HLS and HDL. It offers HLS style of coding but in same time it allows you to manipulate with HDL objects. It means it is little bit slower to write a prototype than you would in HLS, but you always know what, how and why is happening.
* Digital circuit simulator with UVM like verification environment (example usage [CAM](https://github.com/Nic30/hwtLib/blob/master/hwtLib/mem/cam_test.py), [structWriter_test.py](https://github.com/Nic30/hwtLib/blob/master/hwtLib/structManipulators/structWriter_test.py))
* Tools for static analysis ([resourceAnalyzer](https://github.com/Nic30/hwt/blob/master/hwt/serializer/resourceAnalyzer/analyzer.py), example usage [cntr_test.py](https://github.com/Nic30/hwtLib/blob/master/hwtLib/samples/arithmetic/cntr_test.py))
* Serializers to export HWT designs into multiple target HDLs ([verilog, VHDL, system-c, IP-core packager, hwt itself...](https://github.com/Nic30/hwt/tree/master/hwt/serializer))

HWT uses hilevel-netlists for internal representation of target design. Optimized netlists are generated from usual code statements, function calls, statements etc (hw processes are automatically resolved). This netlist is easy to use and easy to modify or analyse by user if there is something missing in main library.
Also [serialization modes](https://github.com/Nic30/hwt/blob/master/hwt/serializer/mode.py) allows to tweaks how component should behave durning serialization.

HWT performs no HLS planing or schedueling. HWT is also good as API for code generating by more advanced tools. Hierarchy of components/interfaces/types is not limited. User specifed names are checked for collision with target language. 

HWT designs are instances. No specific exceution is required, just use toRtl metod or other (take a look at [examples](https://github.com/Nic30/hwtLib/blob/master/hwtLib/)).


## HWT ecosystem

* [hwtLib](https://github.com/Nic30/hwtLib) - Library full of examples and real designs.
* [sphinx-hwt](https://github.com/Nic30/sphinx-hwt) - Plugin for sphinx documentation generator which adds shematic into html documentaion. 
* [hdlConvertor](https://github.com/Nic30/hdlConvertor) - (System) Verilog/VHDL parser
* [hwtHls](https://github.com/Nic30/hwtHls) - High Level Synthetizer (alghorithmic description -> RTL)
* [hwtHdlParsers](https://github.com/Nic30/hwtHdlParsers) (not maintained)- (System) Verilog/VHDL compatibility layer at which allows you to import objects from HDL.


## Installation

This library is regular python package. You can install it using:
```
# system-wide, use -u for local use only
sudo pip3 install hwt
```

Then you are able to use functions and classes defined in hwt library from python console or script.
Installation of [hwtLib](https://github.com/Nic30/hwtLib) is recomended as it contains all interfaces agents etc...


## Similar projects

* [chisel](https://chisel.eecs.berkeley.edu/) - 2012-?, Scala, Hardware metalanguage
* [migen](https://github.com/m-labs/migen) - 2013-?, Python, Hardwre metalanguage 
* [myhdl](https://github.com/myhdl/myhdl) - 2011-?, Python, Process based hardware description language
* [pymtl](https://github.com/cornell-brg/pymtl) - 2014-?, Python, Hardware metalanguage
* [veriloggen](https://github.com/PyHDI/veriloggen) - 2015-?, Python, Verilog centric Hardware metalanguage with HLS like features
* [magma](https://github.com/phanrahan/magma/) - 2017-?, Python, Hardware metalanguage
* [garnet](https://github.com/StanfordAHA/garnet) -2018-?, Python, Coarse-Grained Reconfigurable Architecture generator based on magma

## Related open-source

* [vtr-verilog-to-routing](https://github.com/verilog-to-routing/vtr-verilog-to-routing)
* [verilator](https://www.veripool.org/wiki/verilator) - Verilog -> C/C++ sim
* [yosys](https://github.com/YosysHQ/yosys) - RTL synthesis framework


## Board support libraries (Potential candidates for public integration)

* [loam](https://github.com/phanrahan/loam) - Buildsystem for magma
* [litex](https://github.com/enjoy-digital/litex) - Buildsystem for migen
