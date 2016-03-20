#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from unittest import TestLoader, TextTestRunner, TestSuite


from vhdl_toolkit.tests.hierarchyExtractor import HierarchyExtractorTC
from vhdl_toolkit.tests.operators import OperatorTC
from vhdl_toolkit.tests.parser import ParserTC

from vhdl_toolkit.tests.synthetisator.value import ValueTC

from vhdl_toolkit.tests.synthetisator.interfaceLevel.interfaceSyntherisatorTC import InterfaceSyntherisatorTC 
from vhdl_toolkit.tests.synthetisator.interfaceLevel.vhdlCodesign import VhdlCodesignTC
from vhdl_toolkit.tests.synthetisator.interfaceLevel.subunitsSynthesisTC import SubunitsSynthesisTC


from vhdl_toolkit.tests.synthetisator.rtlLevel.optimalizator import Expr2CondTC
from vhdl_toolkit.tests.synthetisator.rtlLevel.synthesis import TestCaseSynthesis


if __name__ == "__main__":
    def testSuiteFromTCs(tcs):
        loader = TestLoader()
        loadedTcs = [loader.loadTestsFromTestCase(tc) for tc in tcs]
        suite = TestSuite(loadedTcs)
        return suite

    suite = testSuiteFromTCs((
        HierarchyExtractorTC,
        ParserTC,
        InterfaceSyntherisatorTC,
        VhdlCodesignTC,
        SubunitsSynthesisTC,
        Expr2CondTC,
        OperatorTC,
        TestCaseSynthesis,
        ValueTC,
    ))
    runner = TextTestRunner(verbosity=2)
    runner.run(suite)
