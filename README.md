# HWToolkit (hwt),
# the library for hardware development in Python
[![Build Status](https://travis-ci.org/Nic30/hwt.svg?branch=master)](https://travis-ci.org/Nic30/hwt)
[![Coverage Status](https://coveralls.io/repos/github/Nic30/hwt/badge.svg?branch=master)](https://coveralls.io/github/Nic30/hwt?branch=master)
[![codecov](https://codecov.io/gh/Nic30/hwt/branch/master/graph/badge.svg)](https://codecov.io/gh/Nic30/hwt)
[![PyPI version](https://badge.fury.io/py/hwt.svg)](http://badge.fury.io/py/hwt)
[![Documentation Status](https://readthedocs.org/projects/hwtoolkit/badge/?version=latest)](http://hwtoolkit.readthedocs.io/en/latest/?badge=latest)
[![Google group](https://img.shields.io/badge/google%20group-online-green.svg)](https://groups.google.com/forum/#!forum/hwt-community)
[![](https://img.shields.io/github/license/Nic30/hwt.svg)](https://github.com/Nic30/hwt)
[![Python version](https://img.shields.io/pypi/pyversions/hwt.svg)](https://img.shields.io/pypi/pyversions/hwt.svg)
[![Join the chat at https://gitter.im/hwt-community/community](https://badges.gitter.im/hwt-community/community.svg)](https://gitter.im/hwt-community/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
[ROADMAP](https://drive.google.com/file/d/1zyegLIf7VaBRyb-ED5vgOMmHzW4SRZLp/view?usp=sharing)

## Keywords

* Metaprogramming (Hardware Construction Language HCL, templatization) + HLS.
* Simulator API, UVM
* Buildtool, IP core generator

## How HWT can help you?

* The lower layer (IR, HDL serializers) is a shield against a problems related to VHDL/Verilog. It is checking for correctness and synthetisability and removing specific of HDLs.
* The system level and HLS layer allows you to quickly build desing generators with advance optimisation techniques of your choice. 
* Simulator API and it's UVM simulation environment is just python object with C++ binding. This makes it easy to use while not sacrificing performance.
* Rich type system can describe also data locality and packet features. This significantly simplifies configuration of component which are working with packets or any data over remote bus.
* HWT is not compiler nor transpiler but it is actually a core library. It contains only necessary stuff and you can can modify/extend any part any time.
  Because the word of HW developement is always full of unexpected situations. 


## Features

* Hardware Construction Language (HCL) (example [simple](https://github.com/Nic30/hwtLib/blob/master/hwtLib/examples/simple.py), [showcase](https://github.com/Nic30/hwtLib/blob/master/hwtLib/examples/showcase0.py)). It is somewhere between HLS and HDL. It offers HLS style of coding but at the same time it allows you to manipulate HDL objects. This means it is a little bit slower to write a prototype than you would in HLS, but you always know what, how and why is happening.
* Digital circuit simulator with UVM like verification environment (example usage [CAM](https://github.com/Nic30/hwtLib/blob/master/hwtLib/mem/cam_test.py), [structWriter_test.py](https://github.com/Nic30/hwtLib/blob/master/hwtLib/structManipulators/structWriter_test.py))
* Tools for static analysis ([resourceAnalyzer](https://github.com/Nic30/hwt/blob/master/hwt/serializer/resourceAnalyzer/analyzer.py), example usage [cntr_test.py](https://github.com/Nic30/hwtLib/blob/master/hwtLib/examples/arithmetic/cntr_test.py))
* Serializers to export HWT designs into multiple target HDLs ([verilog, VHDL, system-c, IP-core packager, hwt itself...](https://github.com/Nic30/hwt/tree/master/hwt/serializer))

HWT uses hilevel-netlists for internal representation of target design. Optimized netlists are generated from usual code statements, function calls, statements etc (hw processes are automatically resolved). This netlist is easy to use and easy to modify or analyse by user if there is something missing in main library.
Also [serialization modes](https://github.com/Nic30/hwt/blob/master/hwt/serializer/mode.py) allows to tweaks how component should behave during serialization.

HWT performs no HLS planing or schedueling. HWT is also good as API for code generating by more advanced tools. Hierarchy of components/interfaces/types is not limited. User specifed names are checked for collision with target language.

HWT designs are instances. No specific exceution is required, just use to_rtl metod or other (take a look at [examples](https://github.com/Nic30/hwtLib/blob/master/hwtLib/)).


## HWT ecosystem

* [netlistDB](https://github.com/HardwareIR/netlistDB) - High performance circuit database, C++
* [hwtLib](https://github.com/Nic30/hwtLib) - Library with examples and real designs.
* [sphinx-hwt](https://github.com/Nic30/sphinx-hwt) - Plugin for sphinx documentation generator which adds interactive shematic into html documentation.
* [hdlConvertor](https://github.com/Nic30/hdlConvertor) - (System) Verilog/VHDL parser
* [hwtHls](https://github.com/Nic30/hwtHls) - High Level Synthetizer (alghorithmic description -> RTL)
* [hwtHdlParsers](https://github.com/Nic30/hwtHdlParsers) (not maintained)- (System) Verilog/VHDL compatibility layer at which allows you to import objects from HDL.
* [cocopy](https://github.com/potentialventures/cocotb) - Verilator simulator - Python binding
* [ipCorePackager](https://github.com/Nic30/ipCorePackager) - IPCore generator (Vivado, Quartus support etc.) automatic specification of interfaces by metaclass description, register map, clk domains etc.
* [pyMathBitPrecise](https://github.com/Nic30/pyMathBitPrecise) - Bit precise integer types.

## Installation

This library is a regular python package. You can install it using:
```
# system-wide, use -u for local use only
sudo pip3 install hwt
```

Then you are able to use functions and classes defined in the hwt library from a python console or script.
Installation of [hwtLib](https://github.com/Nic30/hwtLib) is recomended as it contains common interfaces, agents, components etc...

## FAQ

* Where is the entry point of the compiler?
  * This is not a compiler, it is library of the objects which can be converted to Verilog/VHDL and back.
* How do I get Verilog/VHDL?
  * Use `to_rtl` method [example](https://github.com/Nic30/hwtLib/blob/master/hwtLib/examples/simple.py)
* How do I define my interface type, protocol and simulation agent?
  * Derive from any Interface class. [example](https://github.com/Nic30/hwt/blob/master/hwt/interfaces/std.py#L107) 
* I do have c structure of UDP header, how do I send/recieve UDP packet over AXI-stream interface?
  * Define HStruct type composed of eth_header_t, IPv4_header_t and HStream(uint8_t) and use [AxisFrameGen](https://github.com/Nic30/hwtLib/blob/master/hwtLib/amba/axis_comp/frameGen.py). There is and example of [ping responder](https://github.com/Nic30/hwtLib/blob/master/hwtLib/examples/builders/pingResponder.py)


## Similar projects

* [autofpga](https://github.com/ZipCPU/autofpga) - C++, A utility for Composing FPGA designs from Peripherals
* [BinPy](https://github.com/BinPy/BinPy) - Python, An electronic simulation library
* [bsc](https://github.com/B-Lang-org/bsc) - Haskell, C++, BSV - Bluespec Compiler 
* [chisel](https://chisel.eecs.berkeley.edu/) - 2012-?, Scala, HCL
* [Chips-2.0](https://github.com/dawsonjon/Chips-2.0) - , , FPGA Design Suite based on C to Verilog design flow
* [concat](https://github.com/conal/concat) - 2016-?, Haskell, Haskell to hardware
* [DUH](https://github.com/sifive/duh) - JS, simple convertor between verilog/scala/ipxact
* [edalize](https://github.com/olofk/edalize) - 2018-?, Python, abstraction layer for eda tools
* [garnet](https://github.com/StanfordAHA/garnet) -2018-?, Python, Coarse-Grained Reconfigurable Architecture generator based on magma
* [hammer](https://github.com/ucb-bar/hammer) - 2017-?, Python, Highly Agile Masks Made Effortlessly from RTL
* [heterocl](https://github.com/cornell-zhang/heterocl) - 2017-?, C++, A Multi-Paradigm Programming Infrastructure for Software-Defined Reconfigurable Computing
* [hoodlum](https://github.com/tcr/hoodlum) - 2016-?, Rust, HCL
* [ILAng](https://github.com/Bo-Yuan-Huang/ILAng) - modeling and verification platform for SoCs where Instruction-Level Abstraction (ILA) is used as the formal model for hardware components.
* [jhdl](https://github.com/larsjoost/jhdl) - ?-2017, C++ Verilog/VHDL -> systemC, prototype
* [Kactus2](http://funbase.cs.tut.fi) - IP-core packager
* [kratos](https://github.com/Kuree/kratos) - C++/Python, hardware generator/simulator
* [lgraph](https://github.com/masc-ucsc/lgraph) - C, generic graph library
* [llhd](https://github.com/fabianschuiki/llhd) - Rust, HCL
* [livehd](https://github.com/masc-ucsc/livehd) - mainly C++, An infrastructure designed for Live Hardware Development.
* [livehd](https://github.com/masc-ucsc/livehd) - JS, utils, infrastructure for Synthesis and Simulation 
* [magma](https://github.com/phanrahan/magma/) - 2017-?, Python, HCL
* [migen](https://github.com/m-labs/migen) - 2013-?, Python, HCL
* [mockturtle](https://github.com/lsils/mockturtle) - logic network library
* [moore](https://github.com/fabianschuiki/moore) - Rust, HDL -> model compiler
* [MyHDL](https://github.com/myhdl/myhdl) - 2004-?, Python, Process based HDL
* [nmigen](https://github.com/m-labs/nmigen) -, Python, A refreshed Python toolbox for building complex digital hardware
* [OpenTimer](https://github.com/OpenTimer/OpenTimer) - , C++,  A High-Performance Timing Analysis Tool for VLSI Systems
* [percy](https://github.com/whaaswijk/percy) - Collection of different synthesizers and exact synthesis methods for use in applications such as circuit resynthesis and design exploration.
* [PyChip-py-hcl](https://github.com/scutdig/PyChip-py-hcl) - , Python, Chisel3 like HCL 
* [pygears](https://github.com/bogdanvuk/pygears) - , Python, function style HDL generator
* [PyMTL3](https://github.com/cornell-brg/pymtl3) 2018-?
* [PyMTL](https://github.com/cornell-brg/pymtl) - 2014-?, Python, Process based HDL
* [PyRTL](https://github.com/UCSBarchlab/PyRTL) - 2015-?, Python, HCL
* [Pyverilog](https://github.com/PyHDI/Pyverilog) - 2013-? Python-based Hardware Design Processing Toolkit for Verilog HDL
* [sail](https://github.com/rems-project/sail) 2018-?, (OCaml, Standard ML, Isabelle) - architecture definition language
* [rogue](https://github.com/slaclab/rogue) , C++/Python - Hardware Abstraction & Data Acquisition System
* [spatial](https://github.com/stanford-ppl/spatial) - Scala, an Argon DSL like, high level abstraction
* [SpinalHDL](https://github.com/SpinalHDL/SpinalHDL) - 2015-?, Scala, HCL
* [SyDpy](https://github.com/bogdanvuk/sydpy) - ?-2016, Python, HCL and verif. framework operating on TML/RTL level
* [systemrdl-compiler](https://github.com/SystemRDL/systemrdl-compiler) - Python,c++, register description language compiler
* [UHDM](https://github.com/alainmarcel/UHDM) - C++ SystemVerilog -> C++ model
* [Verilog.jl](https://github.com/interplanetary-robot/Verilog.jl) - 2017-2017, Julia, simple Julia to Verilog transpiler
* [veriloggen](https://github.com/PyHDI/veriloggen) - 2015-?, Python, Verilog centric HCL with HLS like features

## Related open-source

* [fusesoc](https://github.com/olofk/fusesoc) - package manager and a set of build tools for FPGA/ASIC development
* [OpenSTA](https://github.com/abk-openroad/OpenSTA) - a gate level static timing verifier
* [RePlAce](https://github.com/abk-openroad/RePlAce) - global placement tool
* [verilator](https://www.veripool.org/wiki/verilator) - Verilog -> C/C++ simulator
* [vtr-verilog-to-routing](https://github.com/verilog-to-routing/vtr-verilog-to-routing)
* [yosys](https://github.com/YosysHQ/yosys) - RTL synthesis framework
* [UHDM](https://github.com/alainmarcel/UHDM) - SV -> C++


## Board support libraries (Potential candidates for public integration)

* [litex](https://github.com/enjoy-digital/litex) - Buildsystem for migen
* [loam](https://github.com/phanrahan/loam) - Buildsystem for magma
* [vivado-boards](https://github.com/Digilent/vivado-boards) - Vivado XML/TCL files with board description
* [nmigen-boards](https://github.com/nmigen/nmigen-boards) - board and connector meta fo nmigen
