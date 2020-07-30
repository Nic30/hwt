from typing import Set, List, Dict, Union, Optional

from hwt.doc_markers import internal
from hwt.hdl.assignment import Assignment
from hwt.hdl.statement import HdlStatement
from hwt.hdl.value import HValue
from hwt.synthesizer.rtlLevel.mainBases import RtlSignalBase


@internal
def fill_stm_list_with_enclosure(parentStm: Optional[HdlStatement],
                                 current_enclosure: Set[RtlSignalBase],
                                 statements: List["HdlStatement"],
                                 do_enclose_for: List[RtlSignalBase],
                                 enclosure: Dict[RtlSignalBase, Union[HValue, RtlSignalBase]])\
        -> None:
    """
    Apply enclosure on list of statements
    (fill all unused code branches with assignments from value specified by enclosure)

    :param parentStm: optional parent statement where this list is some branch
    :param current_enclosure: list of signals for which this statement list is enclosed
    :param statements: list of statements
    :param do_enclose_for: selected signals for which enclosure should be used
    :param enclosure: enclosure values for signals

    :attention: original statements parameter can be modified
    :return: new statements
    """
    if statements is None:
        statements = []

    for e_sig in do_enclose_for:
        if e_sig in current_enclosure:
            continue
        enclosed = False
        for stm in statements:
            if e_sig in stm._outputs:
                if e_sig not in stm._enclosed_for:
                    stm._fill_enclosure(enclosure)
                enclosed = True
                break
        # any statement was not related with this signal,
        if not enclosed:
            e = enclosure[e_sig]
            a = Assignment(e, e_sig)
            statements.append(a)

            if parentStm is not None:
                a._set_parent_stm(parentStm)

    return statements
