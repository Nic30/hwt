from typing import List

from hwt.doc_markers import internal
from hwt.hdl.statements.statement import HdlStatement
from hwt.synthesizer.rtlLevel.mainBases import RtlSignalBase


@internal
def HdlStatement_cut_off_drivers_of_list(sig: RtlSignalBase,
                             statements: List[HdlStatement],
                             keep_mask: List[bool],
                             new_statements: List[HdlStatement]):
    """
    Cut all logic from statements which drives signal sig.

    :param sig: signal which drivers should be removed
    :param statements: list of statements to filter
    :param keep_mask: list of flags if True statements was driver only of sig
    :param new_statements: output list of filtered statements

    :return: True if all input statements were reduced
    """
    all_cut_off = True
    for stm in statements:
        newStm = stm._cut_off_drivers_of(sig)
        keep = True
        if newStm is None:
            # statement is des not have drivers of sig
            all_cut_off = False
        elif newStm is stm:
            # statement drives only sig
            keep = False
            new_statements.append(newStm)
        else:
            # statement was splited on multiple statements
            all_cut_off = False
            new_statements.append(newStm)

        keep_mask.append(keep)

    return all_cut_off
