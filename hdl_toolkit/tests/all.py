#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from unittest import TestLoader, TextTestRunner, TestSuite

from hdl_toolkit.tests.hierarchyExtractor import HierarchyExtractorTC
from hdl_toolkit.tests.operators import OperatorTC
from hdl_toolkit.tests.parser import ParserTC

from hdl_toolkit.tests.synthetisator.value import ValueTC

from hdl_toolkit.tests.synthetisator.interfaceLevel.interfaceSyntherisatorTC import InterfaceSyntherisatorTC 
from hdl_toolkit.tests.synthetisator.interfaceLevel.vhdlCodesign import VhdlCodesignTC
from hdl_toolkit.tests.synthetisator.interfaceLevel.verilogCodesign import VerilogCodesignTC
from hdl_toolkit.tests.synthetisator.interfaceLevel.subunitsSynthesisTC import SubunitsSynthesisTC


from hdl_toolkit.tests.synthetisator.rtlLevel.optimalizator import Expr2CondTC
from hdl_toolkit.tests.synthetisator.rtlLevel.synthesis import TestCaseSynthesis
from hdl_toolkit.tests.statementTrees import StatementTreesTC


if __name__ == "__main__":
    def testSuiteFromTCs(*tcs):
        loader = TestLoader()
        loadedTcs = [loader.loadTestsFromTestCase(tc) for tc in tcs]
        suite = TestSuite(loadedTcs)
        return suite

    suite = testSuiteFromTCs(
        HierarchyExtractorTC,
        ParserTC,
        InterfaceSyntherisatorTC,
        VhdlCodesignTC,
        VerilogCodesignTC,
        SubunitsSynthesisTC,
        Expr2CondTC,
        OperatorTC,
        TestCaseSynthesis,
        ValueTC,
        StatementTreesTC,
    )
    runner = TextTestRunner(verbosity=2)
    runner.run(suite)
