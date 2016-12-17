# HWToolkit
[![Join the chat at https://gitter.im/HWToolkit/Lobby](https://badges.gitter.im/HWToolkit/Lobby.svg)](https://gitter.im/HWToolkit/Lobby?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)[![PyPI version](https://badge.fury.io/py/hwt.svg)](http://badge.fury.io/py/hwt) [![Travis-ci Build Status](https://travis-ci.org/Nic30/hwtLib.png?branch=master)](https://travis-ci.org/Nic30/hwtLib)


Main purpose of HWToolkit framework is to speedup FPAGA design development. HWToolkit does the thing by intuitive HW description, powerful macro language, integrated UVM like verification environment.
We know how that importing of other designs is must-have. HWToolkit can import and export designs to many formats like VHDL/Verilog/IPcore/VivadoHLS/MyHdl.
Verification environment has it's own simulator, but can be exported to VHDL/Verilog to allow use with others simulators like Modelsim or Vivado.

We see the fact that many peoples are actually generating HDL code from they'r code generator or by HLS. HWToolkit is kind of overlay over HDL languages which solves problems of HDL languages for you. That means that if you are building code generator you can get rid off HDL problems and work with object representation of abstract code instead.

This part of HWToolkit is used in many optimizers/code navigators.    

* There is library full of examples and real designs at https://github.com/Nic30/hwtLib.
* (System) Verilog/VHDL compatibility layer at https://github.com/Nic30/hwtHdlParsers which allows you to import objects from HDL. 

We also have buildsystem. It does currently support only Xilinx Vivado and can control Modelsim and Altium designer.
