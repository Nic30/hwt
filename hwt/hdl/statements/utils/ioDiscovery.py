from typing import List, Set

from hwt.doc_markers import internal
from hwt.hdl.statements.utils.listOfHdlStatements import ListOfHdlStatement
from hwt.synthesizer.rtlLevel.mainBases import RtlSignalBase


@internal
def HdlStatement_discover_enclosure_for_statements(
        statements: ListOfHdlStatement,
        outputs: List[RtlSignalBase]) -> Set[RtlSignalBase]:
    """
    Discover enclosure for list of statements

    :param statements: list of statements in one code branch
    :param outputs: list of outputs which should be driven from this statement list
    :return: set of signals for which this statement list have always some driver
        (is enclosed)
    """
    result = set()
    if not statements:
        return result

    for stm in statements:
        stm._discover_enclosure()

    for o in outputs:
        has_driver = False

        for stm in statements:
            if o in stm._outputs:
                assert not has_driver
                has_driver = False
                result.update(stm._enclosed_for)
            else:
                pass

    return result

