# HWToolkit
[![Travis-ci Build Status](https://travis-ci.org/Nic30/hwtLib.png?branch=master)](https://travis-ci.org/Nic30/hwtLib) [![PyPI version](https://badge.fury.io/py/hwt.svg)](http://badge.fury.io/py/hwt) [![Join the chat at https://gitter.im/HWToolkit/Lobby](https://badges.gitter.im/HWToolkit/Lobby.svg)](https://gitter.im/HWToolkit/Lobby?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge) 


Main purpose of HWToolkit framework is to speed up FPAGA design development. HWToolkit does the thing by intuitive HW description, powerful macro language, integrated UVM like verification environment and integration with others commonly used tools.
HWToolkit can import and export designs to many formats like VHDL/Verilog/IPcore/VivadoHLS/MyHdl.
Verification environment has it's own simulator, but verification can be exported to VHDL/Verilog as testbench to allow use with others simulators like Modelsim or Vivado.

We see the fact that many peoples are actually generating HDL code from they'r code generator or by HLS in these days.
HWToolkit is kind of overlay over HDL languages which solves problems of HDL languages for you. That means that if you are building code generator you can get rid off HDL problems and work with object representation of abstract code instead (That is why HWT was originally written).
This part of HWToolkit is used in many optimizers/code navigators.    

* There is library full of examples and real designs as well at https://github.com/Nic30/hwtLib.
* (System) Verilog/VHDL compatibility layer at https://github.com/Nic30/hwtHdlParsers which allows you to import objects from HDL. 

We also have buildsystem. It does currently support only Xilinx Vivado and can control Modelsim and Altium designer.
