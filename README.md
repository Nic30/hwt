# HWToolkit
HLS syntetizator, HDL parser writen in python

This library allows you rapidly speedup design creation by abstraction over HDL lanuages, 
it allows you write clean design using hi-level interfaces, 
so you do not have to mess with every signal separately (for the rest of functionality I did not made public examples yet).
Currently library is used for gluing things together. Examples showing this features are placed in /hdl_toolkit/samples/iLvl.

Automatic interface/parameter extraction is implemented take look at /hdl_toolkit/interfaces

Libary has vhdl, verilog, vivado hls/hlx support, object from this langues (entity, architecture, package, function, module ...) 
can be imported and used (take look at  /hdl_toolkit/samples/) like any others. 

## Library components

Unit/UnitFromHdl/VivadoHLSUnit/... - these are main parts of the design. Properties of this objects which are derived from class Interface
or class Param (generic/attribute representation in this library) are recognized by library and they can be synthetised.

HdlSimulator is working but it needs better format than VCD in order to be something.
Hls part is under construction.
IP core packager with automatic gui generator is fully working.
vivado_toolit contains realtime driver for vivado and constrains generator.

### You need to know only this, rest you can see in examples:
* Every unit is like hi-level netlist.

* In _config(self) function you should specify things which can be configured from top.

* In _declr(self)  function you should declare all things on which is configuration applied on,
you can access things from _config(self).

* In _impl(self) you implement internal structure of the unit.

* Interfaces does not have _impl method, rest is same.

* _config(self) is called by constructor by default

* Direction of interfaces are resolved from drivers of interface.

* Easiest way how to extract Unit from VHDL/Verilog is to use UnitFromHdl class (as is shown in examples)
 In order to extract newly defined interface as well UnitFromHdl has 

* Easiest way how to connect is two things is use connect function as shown in examples. 

* Keep in mind that everything is configured from top to bottom but builded in oposite direction.
  This mean you can set configuration for childs in _declr(self) of parent but childs declarations
  and implementation will be completed in parent _impl(self)


This is developement repo not everything needs to be working everytime, check it by running test in package you need. 
Take a look at samples in packages.

The library functionaly is in general driven by my projects usualy at Faculty of Information Technology 
Brno University of Technology.
I know I have to write wiki, but I do not even have time to exists.

The project is licensed under MIT.
