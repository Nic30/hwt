#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from unittest import TestLoader, TextTestRunner, TestSuite
from vhdl_toolkit.tests.synthetisator.interfaceLevel.interfaceSyntherisatorTC import InterfaceSyntherisatorTC 
from vhdl_toolkit.tests.synthetisator.interfaceLevel.vhdlCodesign import VhdlCodesignTC 
from vhdl_toolkit.tests.synthetisator.rtlLevel.optimalizator import Expr2CondTC 
from vhdl_toolkit.tests.operators import OperatorTC
from vhdl_toolkit.tests.synthetisator.rtlLevel.synthesis import TestCaseSynthesis
from vhdl_toolkit.tests.hierarchyExtractor import HierarchyExtractorTC
from vhdl_toolkit.tests.parser import ParserTC

if __name__ == "__main__":

    loader = TestLoader()
    suite = TestSuite((
        loader.loadTestsFromTestCase(HierarchyExtractorTC),
        loader.loadTestsFromTestCase(ParserTC),
        loader.loadTestsFromTestCase(InterfaceSyntherisatorTC),
        loader.loadTestsFromTestCase(VhdlCodesignTC),
        loader.loadTestsFromTestCase(Expr2CondTC),
        loader.loadTestsFromTestCase(OperatorTC),
        loader.loadTestsFromTestCase(TestCaseSynthesis),
    ))

    runner = TextTestRunner(verbosity=2)
    runner.run(suite)
