"""
This package contains HDL types (e.g. HBits), value classes
and conversion functions for them.

The HWT typesystem is similar to C typesystem but there are some key differences:

* The HWT does have an explicit pointer or reference type, instead it uses signals
  or HBits (int) representation of address
* Every HWT type is packed (the structures are represented in memory as they are written,
  there is no automatic padding or alignment logic)
* The HWT HStruct/HUnion members may have name set to None, which denotes the padding.
* The HWT has HStream type. This type can have variable data size and specifies possible alignment
  and size combinations. This is required for packet processing in general as it allows for description
  of the format of the packets.

HWT types are divided into:
 * :note: There are no restrictions on use of anything from python.
   This list of types referes to a types for RtlSignal/HConst classes which are used to build
   a circuit.

 * Types with physical representation
   * :class:`hwt.hdl.types.bits.HBits` - int/bit vector, signed/unsigned/no-signed, to VHDL/Verilog
   
     * There are several commonly used definitions in :mod:`hwtLib.types.ctypes`
       (e.g. :py:attr:`hwtLib.types.ctypes.uint8_t`)
       and in :mod:`hwt.hdl.types.defs` (e.g. :py:attr:`hwt.hdl.types.defs.BIT`)

     * The type may have several flags which control endianity, default casting rules and negations :see: :class:`hwt.hdl.types.bits.HBits`

   * :class:`hwt.hdl.types.array.HArray` - fixed size array of any type, natively converted to VHDL/Verilog
   * :class:`hwt.hdl.types.struct.HStruct` - fixed size struct type. Member name=None denotes padding.
   
 * Types witout physical representation (only for HDL compatibility, no synthetizable operands)
   * :class:`hwt.hdl.types.float.HFloat` - intended for generics/params only
   * :class:`hwt.hdl.types.slice.HSlice` - result of to/downto operator which 
      does not have explicit type in VHDL/Verilog
   * :class:`hwt.hdl.types.string.HString` - intended for generics/params only

 * Types with multiple physical representations which has to be picked compiletime
   * :class:`hwt.hdl.types.enum.HEnum` - natively supported in VHLD, lowered to HBits in Verilog
   * :class:`hwt.hdl.types.stream.HStream` - template of the frame which has to be lowered before HW construction
   * :class:`hwt.hdl.types.union.HUnion` - syntax shugar

 
For practical examples see :class:`hwtLib.examples.tutorialTypesystem_test.TutorialTypesystemTC`

The types in HWT are implemented as a type class which inherits from :class:`hwt.hdl.types.hdlType.HdlType`,
RtlSignal class which interits form :class:`hwt.synthesizer.rtlLevel.rtlSignal.RtlSignal`
and a HConst class which inherits from :class:`hwt.hdl.const.HConst`. 
These classes are linked together using :meth:`hwt.hdl.types.hdlType.HdlType.getConstCls`, 
:meth:`hwt.hdl.types.hdlType.HdlType.getRtlSignalCls`
defined on type class. Note that the type class behaves as a template of the HDL type and
the HDL type itself is an instance of this class.

The supported operators/functions are entrirely define by type RtlSignal/HConst class for a given HdlType.

The type itself does not need any kind of registration in HWT. That means that user can freely define custom types
and use them in design. Also note that the mentioned classes are regular python classes and inheritance
works as expected, meaning that the current types can be extended as well.


Casting rules
==============

* If conversion is not applicable TypeConversionErr or NotImplementedError is raised
* Any cast to same type is always allowed and does nothing.

:see: doc of type classes like :class:`hwt.hdl.types.bits.HBits` for detail, this is just overview

auto_cast
---------
* same type same type with just minor differences.  e.g. name, HBits.negated/force_vector/... flags

explicit_cast
-------------
* cast to a friendly type e.g. HBits with different sign/width/precission etc.


reinterpret_cast
----------------
* reinterpret_cast takes raw bits of value and reinterprets them as a value of the same type.
  This implies that the width of the type must be the same and type has to have physical
  representation. e.g. HStruct to HBits

* HFloat, HSlice, HString do not have physical representation thus they do not support
  reinterpret_cast.

* HStream, HEnum and HUnion do not have fixed physical representation thus they also
  do not support reinterpret_cast.
 
 reinterpret_cast      |HArray  HBits   HStruct HUnion, HEnum, HUnion
 ======================|======= ======= ======= =====================
 HArray                |y       y       y       n
 HBits                 |y       y       y       n         
 HStruct               |y       y       y       n
 HUnion, HEnum, HUnion |n       n       n       n

"""

