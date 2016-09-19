# HWToolkit
HLS syntetizator writen in python (with VHDL/(System) Verilog parser, simulator, UVM like environment, IP core packager ... )

This library was originaly syntax shugar/macro language for vhdl.
Main purpose was to optimize learning curve of VHDL/Verilog and allow rapid developing.
Now library has it's own simulator and it has become hdl language.
It more hi-level abstraction over hardware but also lets you access the lowest layers.
Every thing which can be written in vhdl (and system verilog) can be also written in HWToolkit except for analog part (which can be emulated and we have no need for integrating it).

This is HDL with ultimate preprocesor, real propgraming language, simulator and HSL under single roof.

There is library full of examples at https://github.com/Nic30/hwtLib.
And (System) Verilog/VHDL compatibility layer at https://github.com/Nic30/hwtHdlParsers which allows you to import objects from HDL. Automatic interface/parameter extraction also is implemented.

We also have buildsystem. It is easily extensible but currently support only Xilinx Vivado and can control Modelsim and Altium designer. We also use it for generating *.xdc (constraints) 

There is also layer for importing object from another languages like Vivado Hls or MyHdl.

IP core packager can automaticaly generate gui generator for setting params on unit it also recognizes standard vivado interfaces.


### Light-speed tutorial:
* There are units (Ram, Cpu) and interfaces connecting them (Signal, Clk, Axi4 etc...).

* Every unit is like hi-level netlist, you should override this methods:

* In _config(self) function you should specify things which can be configured from top.

* In _declr(self)  function you should declare all things on which is configuration applied on, you can access things from _config(self).

* In _impl(self) you implement internal structure of the unit.

* Interfaces does not have _impl method, rest is same.

* Direction of interfaces are resolved from drivers of interface and you do not have to wory about it.

* power operator ** is used as connection operator (assign in Verilog, <= in VHDL), there is also function connect with can fit widths. 

* Keep in mind that everything is configured from top to bottom but builded in oposite direction. This mean you can set configuration for childs in _declr(self) of parent but childs declarations and implementation will be completed in parent _impl(self). Result of this is that you can easily configure design but errors are showing up when you try to use them.
 
Take a look at samples in packages and https://github.com/Nic30/hwtLib.

I know I have to write wiki, but I do not even have time to exists.
