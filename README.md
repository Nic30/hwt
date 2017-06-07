# HWToolkit
[![Travis-ci Build Status](https://travis-ci.org/Nic30/hwtLib.png?branch=master)](https://travis-ci.org/Nic30/hwtLib) 
[![Coverage Status](https://coveralls.io/repos/github/Nic30/HWToolkit/badge.svg?branch=master)](https://coveralls.io/github/Nic30/HWToolkit?branch=master)
[![PyPI version](https://badge.fury.io/py/hwt.svg)](http://badge.fury.io/py/hwt) 
[![Documentation Status](https://readthedocs.org/projects/hwtoolkit/badge/?version=latest)](http://hwtoolkit.readthedocs.io/en/latest/?badge=latest) 
[![Join the chat at https://gitter.im/HWToolkit/Lobby](https://badges.gitter.im/HWToolkit/Lobby.svg)](https://gitter.im/HWToolkit/Lobby?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)


HWToolkit is:

* collection of classes which are some form of information about hardware property like
  RtlSignal, RtlNetlist, HdlType etc. and there low level objects are then used in more
  abstract classes like Interface, Unit, AxiStream, Fifo etc.

  * This creates clear hierarchy of objects which is the representation of hardware which 
    can be then serialized to VHDL/Verilog and others. 

* digital circuit simulator with UVM like verification environment

Also keep in mind that HWT itself is usualy used just like api for code generating by more adwanced tools.
Take look at hwtLib where are many useful components. 
There are may HLS like features like:
* loop/FSM generators, function calls in hw (look at hwt.code)
* stream/bus builders (search for Builder)
* abstract structure manipulation and mapping to streams/memories/busses (search for Factory, Parser, StructEndpoint)


* There is library full of examples and real designs as well at https://github.com/Nic30/hwtLib.
* (System) Verilog/VHDL compatibility layer at https://github.com/Nic30/hwtHdlParsers which allows you to import objects from HDL. 
