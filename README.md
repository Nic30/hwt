# HWToolkit
[![Build Status](https://travis-ci.org/Nic30/HWToolkit.svg?branch=master)](https://travis-ci.org/Nic30/HWToolkit)
[![Coverage Status](https://coveralls.io/repos/github/Nic30/HWToolkit/badge.svg?branch=master)](https://coveralls.io/github/Nic30/HWToolkit?branch=master)
[![PyPI version](https://badge.fury.io/py/hwt.svg)](http://badge.fury.io/py/hwt) 
[![Documentation Status](https://readthedocs.org/projects/hwtoolkit/badge/?version=latest)](http://hwtoolkit.readthedocs.io/en/latest/?badge=latest) 
[![Join the chat at https://gitter.im/HWToolkit/Lobby](https://badges.gitter.im/HWToolkit/Lobby.svg)](https://gitter.im/HWToolkit/Lobby?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

## HWToolkit is library for hardware developement, it contains:

* hardware description language
* digital circuit simulator with UVM like verification environment
* tolls for static analisis
* serializers to export HWT designs into multiple target HDLs

## Ideology

* HWT uses netlist for representation of target design.
* It is typical that this netlist are used on multiple levels (stream, data dependency, signals...)
* Netlists are generated from usual code like statements, function calls etc.
* HWT is not hidding reality, parts of netlists are registered on it's parents and are directly visible to user
  as signals. Everything whtat HWT have strict order and reliable behaviour. (=Very unusual for HLS like code generators)
* Netlist can be simulated directly but they are optimalized before simulation (converted to SimModel or SystemC)
* For HWT size does not matter.


Typical flow is:
* Stream netlist description provide by user -> RtlNetlist -> architecture -serializer-> target HDL.


Also keep in mind that HWT itself is usualy used just like api for code generating by more adwanced tools.
* There is library full of examples and real designs as well at https://github.com/Nic30/hwtLib (for hwt is like stdlib for C).
* (System) Verilog/VHDL compatibility layer at https://github.com/Nic30/hwtHdlParsers which allows you to import objects from HDL (not maintained). 


## Similar projects:

https://chisel.eecs.berkeley.edu/

https://github.com/m-labs/migen

https://github.com/myhdl/myhdl

https://github.com/enjoy-digital/litex
