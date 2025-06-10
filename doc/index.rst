Welcome to hwt (HWToolkit) generated documentation!
===================================================

This documentation is automatically generated from actual source code.

What is hwt (HWToolkit)
-----------------------

* Is a Hardware Construction Framework. It is similar to a HCLs like Chisel3 but it is rather set of object with a normal
  behavior rather than a new language. The objects represents signals and other RTL components and can be serialized to Verilog/VHDL/SystemC/...
  (That means the hwt is not transpiler or compiler and there is also no entry point.)

* HWT internal representation is graph database of statements and signals.
  Hwt type system is made of several elemental datatypes templates which can be used for a type of signal:

  * HBits - represents bit vector

  * HStruct - structure/record datatype

  * HUnion - union datatype

  * HArray - array datatype

  * TransTmpl metatype - transactional template which describes how data can be partitioned to memores, buses, streams etc.
  	Think of it like a object which tells how to build frames from potentially sparse data structure in memory.

  * The type itself drives it's hw representation, that means the typesystem is user extensible.

* HWT is build as abstraction layer over all HDL languages to shield users from tricky features of such a languages.
  However nothings is sacrificed and everything can be overridden.

* HWT uses UVM like verification environment implemented in hwtSimApi. hwtSimApi can use verilator or python based simulator
  to achieve high-speed simulation or nearly-zero simulator spin-up.

* Most of parts of HWT ecosystem are independent and you can use them separately.

Other useful libraries
-----------------------

.. image:: _static/hwt_ecosystem_packages.png

Where to start
--------------

Tutorial is in hwtLib.examples.*, every file in this module contains user-entry-level comments.
E.g. hwtLib.examples.simple.SimpleHwModule is a good starting point.

Component in HWT is a class which inherits from HwModule class.
Object of such a class can be converted to a vhdl/Verilog by from hwt.synth.to_rtl function.
That said, this library is regular python library without any non-pyhon dependencies,
it does not have any executable file.

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
