# HWToolkit (hwt),
# the library for hardware development in Python
[![Build Status](https://travis-ci.org/Nic30/hwt.svg?branch=master)](https://travis-ci.org/Nic30/hwt)
[![Coverage Status](https://coveralls.io/repos/github/Nic30/hwt/badge.svg?branch=master)](https://coveralls.io/github/Nic30/hwt?branch=master)
[![PyPI version](https://badge.fury.io/py/hwt.svg)](http://badge.fury.io/py/hwt) 
[![Documentation Status](https://readthedocs.org/projects/hwtoolkit/badge/?version=latest)](http://hwtoolkit.readthedocs.io/en/latest/?badge=latest) 
[![Python version](https://img.shields.io/pypi/pyversions/hwt.svg)](https://img.shields.io/pypi/pyversions/hwt.svg)

## Features:
* Hardware Description Language (example [showcase0.py](https://github.com/Nic30/hwtLib/blob/master/hwtLib/samples/showcase0.py) )

* Digital circuit simulator with UVM like verification environment (example usage [structWriter_test.py](https://github.com/Nic30/hwtLib/blob/master/hwtLib/structManipulators/structWriter_test.py))

* Tools for static analysis ([resourceAnalyzer](https://github.com/Nic30/hwt/blob/master/hwt/serializer/resourceAnalyzer/analyzer.py), example usage [cntr_test.py](https://github.com/Nic30/hwtLib/blob/master/hwtLib/samples/arithmetic/cntr_test.py))

* Serializers to export HWT designs into multiple target HDLs (multiple standards [verilog, VHDL, system-c, IP-core packager, hwt itself...](https://github.com/Nic30/hwt/tree/master/hwt/serializer))

HWT uses netlists for representation of target design. Optimized netlists are generated from usual code statements, function calls, statements etc. HWT performs no HLS planing or schedueling HWT itself is API for code generating by more advanced tools, but it is easy to use it directly.

Other parts of hwt ecosystem:

* [hwtLib](https://github.com/Nic30/hwtLib) - Library full of examples and real designs.

* [sphinx-hwt](https://github.com/Nic30/sphinx-hwt) - plugin for sphinx documentation generator which adds shematic into html documentaion. 

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


## Example, Axi4Lite adress decoder generated from c-like struct description of address space.

* hwtLib contains abstract class called BusEndpoint. Object from this class uses c-like-structure as description of memory space. The goal is create a memory space decoder for any interface just from c-like structure description. This allows for example to switch design from Avalon or Axi to PCI-e in just one line of code. And also c-structure-like description of memory space is very user friendly and greatly reduces the possible errors in design. 
 
* AxiLiteEndpoint is derived from BusEndpoint class and implements slave decoder for AxiLite bus
(AxiLiteEndpoint is component which takes c-like-struct and generates address encoder). It is also possible to specify meta in struct description to specify output interface explicitly.

```python
from hwt.synthesizer.utils import toRtl
from hwt.serializer.vhdl.serializer import VhdlSerializer
from hwt.hdl.types.struct import HStruct
from hwtLib.types.ctypes import uint32_t, uint16_t
from hwtLib.amba.axiLite_comp.endpoint import AxiLiteEndpoint

t = HStruct(
    (uint32_t[4], "data0"),
    # optimized address selection because data are aligned
    (uint32_t[4], "data1"),
    (uint32_t[2], "data2"),
    (uint32_t, "data3"),
    # padding
    (uint32_t[32], None),
    # type can be any type
    (HStruct(
        (uint16_t, "data4a"),
        (uint16_t, "data4b"),
        (uint32_t, "data4c")
    ), "data4"),
)

u = AxiLiteEndpoint(t)

# configuration
u.ADDR_WIDTH.set(8)
u.DATA_WIDTH.set(32)

# convert unit instance to target HDL
print(toRtl(u, serializer=VhdlSerializer))
# print interfaces just for demonstration
print(u.bus)

# decoded interfaces for data type will have same structure as c-struct description (but it is interface)
print(u.decoded.data3)
print(u.decoded.data4)
```

Expected output (trimmed):
```vhdl
--
--    Delegate request from AxiLite interface to fields of structure
--    write has higher priority
--    
library IEEE;
use IEEE.std_logic_1164.all;
use IEEE.numeric_std.all;

ENTITY AxiLiteEndpoint IS
    GENERIC (ADDR_WIDTH: INTEGER := 8;
        DATA_WIDTH: INTEGER := 32;
        decoded_data0_ADDR_WIDTH: INTEGER := 2;
...
    );
    PORT (bus_ar_addr: IN STD_LOGIC_VECTOR(ADDR_WIDTH - 1 DOWNTO 0);
        bus_ar_ready: OUT STD_LOGIC;
        bus_ar_valid: IN STD_LOGIC;
...
        decoded_data0_addr: OUT STD_LOGIC_VECTOR(decoded_data0_ADDR_WIDTH - 1 DOWNTO 0);
        decoded_data0_din: OUT STD_LOGIC_VECTOR(DATA_WIDTH - 1 DOWNTO 0);
        decoded_data0_dout: IN STD_LOGIC_VECTOR(DATA_WIDTH - 1 DOWNTO 0);
        decoded_data0_en: OUT STD_LOGIC;
        decoded_data0_we: OUT STD_LOGIC;
...
<AxiLite, name=bus, _masterDir=DIRECTION.OUT>
<RegCntrl, name=decoded.data3, _masterDir=DIRECTION.OUT>
<StructIntf, name=decoded.data4, _masterDir=DIRECTION.OUT>
```



## Similar projects:

https://chisel.eecs.berkeley.edu/

https://github.com/m-labs/migen

https://github.com/myhdl/myhdl

https://github.com/enjoy-digital/litex

https://github.com/cornell-brg/pymtl

https://github.com/YosysHQ/yosys

https://github.com/PyHDI/veriloggen

https://github.com/StanfordAHA/garnet

https://github.com/phanrahan/magmathon


## Board support libraries (Potential candidates for public integration):

https://github.com/phanrahan/loam

