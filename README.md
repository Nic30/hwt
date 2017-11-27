# HWToolkit (hwt),
# the library for hardware developement in Python
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
* There is library full of examples and real designs as well at [hwtLib](https://github.com/Nic30/hwtLib) (for hwt is like stdlib for C).
* (System) Verilog/VHDL compatibility layer at [hwtHdlParsers](https://github.com/Nic30/hwtHdlParsers) which allows you to import objects from HDL (not maintained).
* There is HDL parser [hdlConvertor](https://github.com/Nic30/hdlConvertor)
* There is prototype (pre alfa) of IDE [hwtIde](https://github.com/Nic30/hwtIde)


## Example

* AxiLiteEndpoint is derived from BusEndpoint class and implements slave decoder for AxiLite bus

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

# type flattening can be specified by shouldEnterFn parameter
# target interface can be overriden by _mkFieldInterface function

# There are other bus endpoints, for example:
# IpifEndpoint, I2cEndpoint, AvalonMmEndpoint and others
# decoded interfaces for data type will be same just bus interface
# will difer
u = AxiLiteEndpoint(t)

# configuration
u.ADDR_WIDTH.set(8)
u.DATA_WIDTH.set(32)

print(toRtl(u, serializer=VhdlSerializer))
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
