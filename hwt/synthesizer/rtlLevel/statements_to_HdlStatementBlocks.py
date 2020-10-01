from copy import copy
from itertools import compress
from typing import Generator, List

from hwt.doc_markers import internal
from hwt.hdl.block import HdlStatementBlock
from hwt.hdl.statement import HwtSyntaxError, HdlStatement
from hwt.hdl.statementUtils import fill_stm_list_with_enclosure
from hwt.hdl.value import HValue
from hwt.pyUtils.uniqList import UniqList
from hwt.synthesizer.rtlLevel.reduce_processes import reduceProcesses
from hwt.synthesizer.rtlLevel.rtlSignal import NO_NOPVAL, RtlSignal


@internal
def cut_off_drivers_of(dstSignal: RtlSignal, statements: List[HdlStatement]):
    """
    Cut off drivers from statements
    """
    separated = []
    stm_filter = []
    for stm in statements:
        stm._clean_signal_meta()
        d = stm._cut_off_drivers_of(dstSignal)
        if d is not None:
            separated.append(d)

        f = d is not stm
        stm_filter.append(f)

    return list(compress(statements, stm_filter)), separated


@internal
def name_for_process(outputs: List[RtlSignal]) -> str:
    """
    Resolve name for process
    """
    out_names = []
    for sig in outputs:
        if not sig.hasGenericName:
            out_names.append(sig.name)

    if out_names:
        return min(out_names)
    else:
        return ""


@internal
def _statements_to_HdlStatementBlocks(_statements, tryToSolveCombLoops)\
        -> Generator[HdlStatementBlock, None, None]:
    assert _statements
    # try to simplify statements
    proc_statements = []
    for _stm in _statements:
        _stm._clean_signal_meta()
        stms, _ = _stm._try_reduce()
        proc_statements.extend(stms)

    if not proc_statements:
        return

    outputs = UniqList()
    _inputs = UniqList()
    sensitivity = UniqList()
    enclosed_for = set()
    _proc_statements = []
    for _stm in proc_statements:
        seen = set()
        _stm._discover_sensitivity(seen)
        _stm._discover_enclosure()
        if _stm._outputs:
            # remove a statement entirely if it has no ouput
            # (empty if statment or something similar)
            # simulation only processes should not be processed by this function
            # and process should always drive something, unless it is useless
            outputs.extend(_stm._outputs)
            _inputs.extend(_stm._inputs)
            sensitivity.extend(_stm._sensitivity)
            enclosed_for.update(_stm._enclosed_for)
            _proc_statements.append(_stm)

    proc_statements = _proc_statements
    if not proc_statements:
        # this can happen e.g. when If does not contains any Assignment
        return
    sensitivity_recompute = False
    enclosure_recompute = False
    enclosure_values = {}
    for sig in outputs:
        # inject nop_val if needed
        if sig._nop_val is not NO_NOPVAL and sig not in enclosed_for:
            enclosure_recompute = True
            n = sig._nop_val
            enclosure_values[sig] = n
            if not isinstance(n, HValue):
                _inputs.append(n)
                sensitivity_recompute = True

    if enclosure_recompute:
        # we have some enclosure values, try fill missing code branches with
        # this values
        do_enclose_for = [o for o in outputs if o in enclosure_values]
        fill_stm_list_with_enclosure(None, enclosed_for, proc_statements,
                                     do_enclose_for, enclosure_values)

    if enclosure_recompute or sensitivity_recompute:
        for _stm in proc_statements:
            _stm._clean_signal_meta()
            seen = set()
            _stm._discover_sensitivity(seen)
            _stm._discover_enclosure()

    if sensitivity_recompute:
        sensitivity = UniqList()
        for _stm in proc_statements:
            sensitivity.extend(_stm._sensitivity)

    for o in outputs:
        assert not o.hidden, o

    seen = set()
    inputs = UniqList()
    for i in _inputs:
        inputs.extend(i._walk_public_drivers(seen))

    intersect = outputs.intersection_set(sensitivity)
    if intersect:
        # there is a combinational loop inside a single process which
        # can not be solved by separation of statments in process
        if not tryToSolveCombLoops:
            raise HwtSyntaxError(
                "Combinational loop on signal(s)", intersect)

        # try to solve combinational loops by separating drivers of signals
        # from statements
        for sig in intersect:
            proc_statements, proc_stms_select = cut_off_drivers_of(
                sig, proc_statements)
            yield from _statements_to_HdlStatementBlocks(proc_stms_select, False)

        if proc_statements:
            yield from _statements_to_HdlStatementBlocks(proc_statements, False)
    else:
        # no combinational loops, wrap current statemetns to a process instance
        name = name_for_process(outputs)
        yield HdlStatementBlock("assig_process_" + name,
                                proc_statements, sensitivity,
                                inputs, outputs)


@internal
def statements_to_HdlStatementBlocks(statements: List[HdlStatement])\
        -> Generator[HdlStatementBlock, None, None]:
    """
    Pack statements into HdlStatementBlock instances,
    * for each out signal resolve it's drivers and collect them
    * split statements if there is and combinational loop
    * merge statements if it is possible
    * resolve sensitivity lists
    * wrap into HdlStatementBlock instance
    * for every IO of process generate name if signal has not any
    """
    # create copy because this set will be reduced
    statements = copy(statements)

    # process ranks = how many assignments is probably in process
    # used to minimize number of merge tries
    processes = []
    while statements:
        stm = statements.pop()
        proc_statements = [stm, ]
        ps = _statements_to_HdlStatementBlocks(proc_statements, True)
        processes.extend(ps)

    yield from reduceProcesses(processes)
