"""
Sythesizer converts :class:`hwt.synthesizer.unit.Unit` instances to HDL objects.

:func:`hwt.synthesizer.utils.to_rtl` function is one of examples how to use this module.
The conversion of :class:`hwt.synthesizer.unit.Unit` instances happens mainly in
:meth:`hwt.synthesizer.unit.Unit._to_rtl` which calls other optmisation and transformations
stored in :Py:attr:`:hwt.synthesizer.unit.Unit._target_platform`.
"""
