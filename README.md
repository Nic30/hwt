# HWToolkit (hwt),
# the library for hardware development in Python
[![Build Status](https://travis-ci.org/Nic30/hwt.svg?branch=master)](https://travis-ci.org/Nic30/hwt)
[![Coverage Status](https://coveralls.io/repos/github/Nic30/hwt/badge.svg?branch=master)](https://coveralls.io/github/Nic30/hwt?branch=master)
[![PyPI version](https://badge.fury.io/py/hwt.svg)](http://badge.fury.io/py/hwt) 
[![Documentation Status](https://readthedocs.org/projects/hwtoolkit/badge/?version=latest)](http://hwtoolkit.readthedocs.io/en/latest/?badge=latest) 
[![Google group](https://img.shields.io/badge/google%20group-online-green.svg)](https://groups.google.com/forum/#!forum/hwt-community)
[![](https://img.shields.io/github/license/Nic30/hwt.svg)](https://github.com/Nic30/hwt)
[![Python version](https://img.shields.io/pypi/pyversions/hwt.svg)](https://img.shields.io/pypi/pyversions/hwt.svg)
[ROADMAP](https://drive.google.com/file/d/1zyegLIf7VaBRyb-ED5vgOMmHzW4SRZLp/view?usp=sharing)

## Keywords

* Metaprogramming (Hardware Construction Language HCL, templatization) + HLS.
* Simulator API, UVM
* Buildtool, IP core generator

## How HWT can help you?
* The lower layer (IR, HDL serializers) is a shield against a problems related to VHDL/Verilog it is checking for correctness and synthetisability and removing specific of HDLs.
* Simulator API - UVM simulation environment as a normal python object, easy to use while not sacrificing performance. Python driven.
* C inspired type system is most important part of HWT as it allows all components use same description and thanks to stream-memory and other component generators significantly simplifies the developement of components which are using complex data structures. The typesystem contains not just struct/union, but also frame templates which can describe spartial data and the creation of the frames from data.
* KISS (Keep it stupid and simple), each functionality separated as independent, but compatible, library so you do not have to care about it if you are not using it. Learning curve optimisation. 
   

## Features

* Hardware Construction Language (HCL) (example [simple](https://github.com/Nic30/hwtLib/blob/master/hwtLib/examples/simple.py), [showcase](https://github.com/Nic30/hwtLib/blob/master/hwtLib/examples/showcase0.py)). It is somewhere between HLS and HDL. It offers HLS style of coding but at the same time it allows you to manipulate HDL objects. This means it is a little bit slower to write a prototype than you would in HLS, but you always know what, how and why is happening.
* Digital circuit simulator with UVM like verification environment (example usage [CAM](https://github.com/Nic30/hwtLib/blob/master/hwtLib/mem/cam_test.py), [structWriter_test.py](https://github.com/Nic30/hwtLib/blob/master/hwtLib/structManipulators/structWriter_test.py))
* Tools for static analysis ([resourceAnalyzer](https://github.com/Nic30/hwt/blob/master/hwt/serializer/resourceAnalyzer/analyzer.py), example usage [cntr_test.py](https://github.com/Nic30/hwtLib/blob/master/hwtLib/examples/arithmetic/cntr_test.py))
* Serializers to export HWT designs into multiple target HDLs ([verilog, VHDL, system-c, IP-core packager, hwt itself...](https://github.com/Nic30/hwt/tree/master/hwt/serializer))

HWT uses hilevel-netlists for internal representation of target design. Optimized netlists are generated from usual code statements, function calls, statements etc (hw processes are automatically resolved). This netlist is easy to use and easy to modify or analyse by user if there is something missing in main library.
Also [serialization modes](https://github.com/Nic30/hwt/blob/master/hwt/serializer/mode.py) allows to tweaks how component should behave during serialization.

HWT performs no HLS planing or schedueling. HWT is also good as API for code generating by more advanced tools. Hierarchy of components/interfaces/types is not limited. User specifed names are checked for collision with target language. 

HWT designs are instances. No specific exceution is required, just use toRtl metod or other (take a look at [examples](https://github.com/Nic30/hwtLib/blob/master/hwtLib/)).


## HWT ecosystem

* [netlistDB](https://github.com/HardwareIR/netlistDB) - High performance circuit database, C++
* [hwtLib](https://github.com/Nic30/hwtLib) - Library with examples and real designs.
* [sphinx-hwt](https://github.com/Nic30/sphinx-hwt) - Plugin for sphinx documentation generator which adds interactive shematic into html documentaion. 
* [hdlConvertor](https://github.com/Nic30/hdlConvertor) - (System) Verilog/VHDL parser
* [hwtHls](https://github.com/Nic30/hwtHls) - High Level Synthetizer (alghorithmic description -> RTL)
* [hwtHdlParsers](https://github.com/Nic30/hwtHdlParsers) (not maintained)- (System) Verilog/VHDL compatibility layer at which allows you to import objects from HDL.
* [cocopy](https://github.com/potentialventures/cocotb) - Verilator simulator - Python binding


## Installation

This library is a regular python package. You can install it using:
```
# system-wide, use -u for local use only
sudo pip3 install hwt
```

Then you are able to use functions and classes defined in the hwt library from a python console or script.
Installation of [hwtLib](https://github.com/Nic30/hwtLib) is recomended as it contains all interfaces agents etc...

## FAQ

* Where is the entry point of the compiler?
  * This is not a compiler, it is library of the objects which can be converted to Verilog/VHDL and back.
* How do I get Verilog/VHDL?
  * Use `toRtl` method [example](https://github.com/Nic30/hwtLib/blob/master/hwtLib/examples/simple.py) 
* How do I define my interface type, protocol and simulation agent?
  * Derive from any Interface class and update `_initSimAgent` to create simulation agent of your type.
* I do have c structure of UDP header, how do I send/recieve UDP packet over AXI-stream interface?
  * Define HStruct type composed of eth_header_t, IPv4_header_t and HStream(uint8_t) and use [AxisFrameGen](https://github.com/Nic30/hwtLib/blob/master/hwtLib/amba/axis_comp/frameGen.py). There is and example of [ping responder](https://github.com/Nic30/hwtLib/blob/master/hwtLib/examples/builders/pingResponder.py) 



## Similar projects

* [chisel](https://chisel.eecs.berkeley.edu/) - 2012-?, Scala, HCL
* [SpinalHDL](https://github.com/SpinalHDL/SpinalHDL) - 2015-?, Scala, HCL
* [migen](https://github.com/m-labs/migen) - 2013-?, Python, HCL
* [Pyverilog](https://github.com/PyHDI/Pyverilog) - 2013-? Python-based Hardware Design Processing Toolkit for Verilog HDL
* [nmigen](https://github.com/m-labs/nmigen) - 
* [jhdl](https://github.com/larsjoost/jhdl) - ?-2017, C++ Verilog/VHDL -> systemC, prototype
* [MyHDL](https://github.com/myhdl/myhdl) - 2004-?, Python, Process based HDL
* [PyMTL](https://github.com/cornell-brg/pymtl) - 2014-?, Python, Process based HDL
* [veriloggen](https://github.com/PyHDI/veriloggen) - 2015-?, Python, Verilog centric HCL with HLS like features
* [hammer](https://github.com/ucb-bar/hammer) - 2017-?, Python, Highly Agile Masks Made Effortlessly from RTL
* [hoodlum](https://github.com/tcr/hoodlum) - 2016-?, Rust, HCL
* [magma](https://github.com/phanrahan/magma/) - 2017-?, Python, HCL
* [garnet](https://github.com/StanfordAHA/garnet) -2018-?, Python, Coarse-Grained Reconfigurable Architecture generator based on magma
* [concat](https://github.com/conal/concat) - 2016-?, Haskell, Haskell to hardware
* [PyRTL](https://github.com/UCSBarchlab/PyRTL) - 2015-?, Python, HCL
* [Verilog.jl](https://github.com/interplanetary-robot/Verilog.jl) - 2017-2017, Julia, simple Julia to Verilog transpiler
* [Kactus2](http://funbase.cs.tut.fi) - IP-core packager
* [edalize](https://github.com/olofk/edalize) - 2018-?, Python, abstraction layer for eda tools
* [sail](https://github.com/rems-project/sail) 2018-?, (OCaml, Standard ML, Isabelle) - architecture definition language 
* [mockturtle](https://github.com/lsils/mockturtle) - logic network library
* [percy](https://github.com/whaaswijk/percy) - Collection of different synthesizers and exact synthesis methods for use in applications such as circuit resynthesis and design exploration.

## Related open-source

* [fusesoc](https://github.com/olofk/fusesoc) - package manager and a set of build tools for FPGA/ASIC development 
* [vtr-verilog-to-routing](https://github.com/verilog-to-routing/vtr-verilog-to-routing)
* [verilator](https://www.veripool.org/wiki/verilator) - Verilog -> C/C++ sim
* [yosys](https://github.com/YosysHQ/yosys) - RTL synthesis framework
* [OpenSTA](https://github.com/abk-openroad/OpenSTA) - a gate level static timing verifier 
* [RePlAce](https://github.com/abk-openroad/RePlAce) - global placement tool 


## Board support libraries (Potential candidates for public integration)

* [loam](https://github.com/phanrahan/loam) - Buildsystem for magma
* [litex](https://github.com/enjoy-digital/litex) - Buildsystem for migen
