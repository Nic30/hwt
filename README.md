# HWToolkit (hwt), the library for hardware developement in Python
[![Build Status](https://travis-ci.org/Nic30/HWToolkit.svg?branch=master)](https://travis-ci.org/Nic30/HWToolkit)
[![Coverage Status](https://coveralls.io/repos/github/Nic30/HWToolkit/badge.svg?branch=master)](https://coveralls.io/github/Nic30/HWToolkit?branch=master)
[![PyPI version](https://badge.fury.io/py/hwt.svg)](http://badge.fury.io/py/hwt) 
[![Documentation Status](https://readthedocs.org/projects/hwtoolkit/badge/?version=latest)](http://hwtoolkit.readthedocs.io/en/latest/?badge=latest) 
[![Join the chat at https://gitter.im/HWToolkit/Lobby](https://badges.gitter.im/HWToolkit/Lobby.svg)](https://gitter.im/HWToolkit/Lobby?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

## hwt contains:

* hardware description language (example [showcase0.py](https://github.com/Nic30/hwtLib/blob/master/hwtLib/samples/showcase0.py) )
* digital circuit simulator with UVM like verification environment (example usage [structWriter_test.py](https://github.com/Nic30/hwtLib/blob/master/hwtLib/structManipulators/structWriter_test.py))
* tolls for static analisis (all design object are acessible to user any time, [resourceAnalyzer](https://github.com/Nic30/HWToolkit/blob/master/hwt/serializer/resourceAnalyzer/analyzer.py), example usage [cntr_test.py](https://github.com/Nic30/hwtLib/blob/master/hwtLib/samples/arithmetic/cntr_test.py))
* serializers to export HWT designs into multiple target HDLs (multiple standards [hwt, verilog, VHDL, system-c](https://github.com/Nic30/HWToolkit/tree/master/hwt/serializer))

## Ideology

* Every part of HWT is optional and can be replaced or ecluded by user, there are no magic classes etc. library is all pythonic.
* HWT uses hierarchy of netlist for representation of target design.
* Optimized netlists are generated from usual code statements, function calls etc.
* HWT performs no HLS planing or schedueling (done in [hwtHls](https://github.com/Nic30/hwtHls) )
* Netlist can be simulated directly but they are optimalized before simulation (converted to SimModel or SystemC)
* HWT can run in parallel in default it runs in single thread and parallelization should be done on level of tests.



Also keep in mind that HWT itself is usualy used just like api for code generating by more adwanced tools.
* There is library full of examples and real designs as well at https://github.com/Nic30/hwtLib (for hwt is like stdlib for C).
* (System) Verilog/VHDL compatibility layer at https://github.com/Nic30/hwtHdlParsers which allows you to import objects from HDL (not maintained).
* There is HDL parser [hdlConvertor](https://github.com/Nic30/hdlConvertor)
* There is prototype (pre alfa) of IDE [hwtIde](https://github.com/Nic30/hwtIde)


## Similar projects:

https://chisel.eecs.berkeley.edu/

https://github.com/m-labs/migen

https://github.com/myhdl/myhdl

https://github.com/enjoy-digital/litex

https://github.com/cornell-brg/pymtl
