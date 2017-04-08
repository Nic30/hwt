Welcome to HWToolkit generated documentation!
=============================================

This documentation is automatically generated from source code on every push into master which pass testing.

HWToolkit is:

* collection of classes which are some form of information about hardware property like
  RtlSignal, RtlNetlist, HdlType etc. and there low level objects are then used in more
  abstract classes like Interface, Unit, AxiStream, Fifo etc.

  * This creates clear hierarchy of objects which is the representation of hardware which 
    can be then serialized to VHDL/Verilog and others. 

* digital circuit simulator with UVM like verification environment


Also keep in mind that HWT itself is just a basic tool which is used to build more advanced tools.
Take look at hwtLib where are many useful components. 
There are may HLS like features like:
* loop/FSM generators, function calls in hw (look at hwt.code)
* stream/bus builders (search for Builder)
* abstract structure manipulation and mapping to streams/memories/busses (search for Factory, Parser, StructEndpoint)


 
You can also download this doc in `PDF
<https://media.readthedocs.org/pdf/hwtoolkit/latest/hwtoolkit.pdf>`_.


.. toctree::
   :maxdepth: 4
   :caption: Contents:

   hwt


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
