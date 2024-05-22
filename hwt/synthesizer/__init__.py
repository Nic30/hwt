"""
Sythesizer converts :class:`hwt.hwModule.HwModule` instances to HDL objects.

:func:`hwt.synth.to_rtl` function is one of examples how to use this module.
The conversion of :class:`hwt.hwModule.HwModule` instances happens mainly in
:meth:`hwt.hwModule.Hmodule._to_rtl` which calls other optimization and transformations
stored in :Py:attr:`:hwt.hwModule.HwModule._target_platform`.
"""
