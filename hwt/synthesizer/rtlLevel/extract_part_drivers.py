from itertools import islice
from typing import Dict, List, Tuple, Union, Optional

from hwt.code import Concat
from hwt.doc_markers import internal
from hwt.hdl.assignment import Assignment
from hwt.hdl.block import HdlStatementBlock
from hwt.hdl.ifContainter import IfContainer
from hwt.hdl.operator import isConst
from hwt.hdl.statement import HdlStatement
from hwt.hdl.switchContainer import SwitchContainer
from hwt.hdl.types.bits import Bits
from hwt.hdl.types.bitsVal import BitsVal
from hwt.hdl.types.defs import SLICE
from hwt.hdl.types.sliceVal import SliceVal
from hwt.hdl.value import HValue
from hwt.serializer.utils import RtlSignal_sort_key, HdlStatement_sort_key
from hwt.synthesizer.rtlLevel.constants import NOT_SPECIFIED
from hwt.synthesizer.rtlLevel.rtlSignal import RtlSignal


def find_independent_slice_drivers(stm: HdlStatement):
    if isinstance(stm, Assignment):
        if stm.indexes and len(stm.indexes) == 1 and isinstance(stm.dst._dtype, Bits):
            dst = stm.dst
            for i in stm.indexes:
                if not isConst(i):
                    return

            can_directly_replace_with_src_expr = stm.parentStm is None
            yield (
                dst,
                tuple(stm.indexes),
                can_directly_replace_with_src_expr,
                stm.src if can_directly_replace_with_src_expr else None
            )
    else:
        for _stm in stm._iter_stms():
            yield from find_independent_slice_drivers(_stm)


def _format_indexes(indexes):
    return tuple(
        (int(i) + 1, int(i))
            if isinstance(i, BitsVal) else
        (int(i.val.start), int(i.val.stop))
        for i in indexes)


def extract_part_drivers_stm(stm: HdlStatement, signal_parts: Dict[RtlSignal, List[Tuple[RtlSignal, List[HValue]]]]):
    if isinstance(stm, Assignment):
        if stm.indexes and len(stm.indexes) == 1:
            dst = stm.dst
            parts = signal_parts.get(dst, None)
            if parts is None:
                return False
            indexes = _format_indexes(stm.indexes)
            new_dsts, do_remove_stm = parts[indexes]
            if isinstance(new_dsts, list):
                assert len(new_dsts) > 1, (dst, new_dsts, stm)
                assert not do_remove_stm, (dst, new_dsts, stm)
                # the driven slice was split to multiple sub slices
                replacement = []
                dst_offset = new_dsts[0][-1][1]
                for i in new_dsts:
                    new_dst = parts[i][0]
                    new_src = stm.src
                    for _i in i:
                        high, low = _i[0] - dst_offset, _i[1] - dst_offset
                        assert high > 0 and low >= 0, dst_offset
                        assert high > low, (dst, stm, (high, low))
                        new_src = new_src[high:low]
                    a = new_dst(new_src)
                    replacement.append(a)

                # it has to hav parent statement because it needs to be nested
                # because otherwise it would not have some overlapping parts driven diferently
                # inder some condition
                stm.parentStm._replace_child_statement(stm, replacement, False)
                return True

            if do_remove_stm:
                # remove current assignment because we are using src directly
                assert stm.parentStm is None, stm
                stm._destroy()
            else:
                # rewrite the Assignment instance to use new dst
                stm._outputs.discard(stm.dst)
                stm._outputs.append(new_dsts)
                stm.dst = new_dsts
                stm.indexes = None
                dst.drivers.append(stm)

            return True

    elif isinstance(stm, (IfContainer, SwitchContainer, HdlStatementBlock)):
        modified = False
        for _stm in stm._iter_stms():
            modified |= extract_part_drivers_stm(_stm, signal_parts)
        if modified:
            assert not stm._enclosed_for, "_enclosed_for is expected not to be initialized yet"
            stm._outputs.clear()
            stm._inputs.clear()
            stm._collect_io()
            return True

    else:
        raise NotImplementedError("Unknown statement ", stm)

    return False


@internal
def construct_tmp_dst_sig_for_slice(dst: RtlSignal, indexes: List[Union[BitsVal, SliceVal]], src: Optional[RtlSignal], is_signal_needed: bool) -> RtlSignal:
    """
    Construct a tmp signal or value which will be used instead of slice from original signal

    :param dst: a signal which slice we want to generate tmp signal for
    :param indexes: a indexes to specify the slice of the dst
    :param is_signal_needed: True if we need a signal which will we drive later, else returns HValue instance
        resolved from default and nop value
    """
    if is_signal_needed:
        name = dst.name

    def_val = dst.def_val
    nop_val = dst._nop_val
    for i in indexes:
        def_val = def_val[i]
        if nop_val is not NOT_SPECIFIED:
            nop_val = nop_val[i]

        if is_signal_needed:
            dst = dst[i]
            if isinstance(i, SliceVal):
                if int(i.val.step) == -1:
                    stop = int(i.val.stop)
                    start = int(i.val.start)
                    name = f"{name}_{start - 1:d}downto{stop:d}"
                else:
                    raise NotImplementedError(i.val.step)
            else:
                _i = int(i)
                name = f"{name:s}_{_i:d}"

    if is_signal_needed:
        tmp_sig = dst.ctx.sig(name, dst._dtype, def_val=def_val, nop_val=nop_val)
        tmp_sig.hidden = False
        tmp_sig.hasGenericName = False
        return tmp_sig
    elif src is not None:
        return src
    elif nop_val is not NOT_SPECIFIED:
        return nop_val
    else:
        return def_val


def resolve_splitpoints(s: RtlSignal, parts):
    split_points = set()
    add_split_point = split_points.add
    for i, _, _ in parts:
        if len(i) != 1:
            raise NotImplementedError(s, i)
        i = i[0]

        if isinstance(i, BitsVal):
            # index is normal integer
            i = int(i)
            add_split_point(i)
            add_split_point(i + 1)
        else:
            # index is slice
            assert isinstance(i, SliceVal), (s, i)
            add_split_point(int(i.val.start))
            add_split_point(int(i.val.stop))

    if isinstance(s._dtype, Bits):
        # add boundary points in the case something is unconnected
        add_split_point(0)
        add_split_point(s._dtype.bit_length())
    else:
        raise NotImplementedError(s._dtype)

    return split_points


def resolve_final_parts_from_splitpoints_and_parts(signal_parts):
    # :type: Dict[RtlSignal, Dict[Tuple[Tuple[int, int], ...], Union[HValue, RtlSignal]]]
    final_signal_parts = {}
    # split part intervals to non-overlapping chunks
    for s, parts in sorted(signal_parts.items(), key=lambda x: RtlSignal_sort_key(x[0])):
        split_point = resolve_splitpoints(s, parts)
        split_point = sorted(split_point)
        # prepare part signals
        new_parts = []
        new_parts_dict = {}
        split_i = 0
        end = 0
        # :attention: parts are likely to contain parts with same indexes
        for indexes, can_directly_replace_with_src_expr, src in sorted(parts, key=lambda x: x[0]):
            if len(indexes) != 1:
                raise NotImplementedError()
            i = indexes[0]
            split_p = split_point[split_i]
            if isinstance(i, BitsVal):
                low = int(i)
                high = low + 1
                index_key = ((high, low), )
            else:
                assert isinstance(i, SliceVal), (s, i)
                if i.val.step != -1:
                    raise NotImplementedError(s, i)
                high, low = int(i.val.start), int(i.val.stop)
                index_key = ((high, low),)

            while split_p < low:
                # some parts at the beginning are skiped
                # that means that that part is not driven by anything
                # and we need to check default and nop value
                part_indexes = (SLICE.from_py(slice(low, split_p , -1)),)
                _src = construct_tmp_dst_sig_for_slice(s, part_indexes, None, True)
                new_parts.append(_src)
                _index_key = ((low, split_p),)
                new_parts_dict[_index_key] = _src, True
                split_i += 1
                split_p = split_point[split_i]


            this_start_split_p_i = split_i
            if split_p > low:
                # some parts at the beginning were already resolved
                # This can happen if there was some part which started on some <= index and overlaps with this part.
                try:
                    _, _can_directly_replace_with_src_expr = new_parts_dict[index_key]
                    assert not _can_directly_replace_with_src_expr, (s, index_key)
                    # was already resolved and checked no need to check it again
                    continue
                except KeyError:
                    pass


                for i in range(split_i, -1, -1):
                    _sp = split_point[i]
                    if _sp == low:
                        this_start_split_p_i = i

            assert split_point[this_start_split_p_i] == low
            # just at the start of this slice
            next_split_p = split_point[this_start_split_p_i + 1]
            assert next_split_p <= high, "The next split point can be at most end of current part"
            if next_split_p == high:
                assert this_start_split_p_i == split_i, "We should see this part for the first time or the split_i should already be higher"
                # all bits on this slice are alwyas driven at once, we can instantiate whole part
                assert split_p == low
                _src = construct_tmp_dst_sig_for_slice(s, indexes, src, not can_directly_replace_with_src_expr)
                new_parts.append(_src)
                new_parts_dict[index_key] = _src, can_directly_replace_with_src_expr
                split_i += 1
            else:
                # list of part keys for later search
                _split_parts = []
                prev_sp = split_point[this_start_split_p_i]
                dst_offset = low
                assert not can_directly_replace_with_src_expr
                # continue instanciating parts until we reach the end of this part
                for sp_i, sp in zip(range(this_start_split_p_i + 1, len(split_point)),
                                    islice(split_point, this_start_split_p_i + 1, None)):
                    # need to generate sub slice
                    # because this slice has actually multiple individualy driven parts

                    # we need to generate all slice parts because there could be a case where only some sub parts are
                    # driven elsewhere and we would othervise resolve those segments as a constantly driven
                    # but they are in fact driven from this slice
                    if sp > high:
                        break

                    part_key = ((sp, prev_sp),)
                    if sp_i <= split_i:
                        # check if the slice is not driven from some top level constant assignment
                        # which would result is multiple drivers of this slice
                        assert src is None
                        existing_part, _can_directly_replace_with_src_expr = new_parts_dict[part_key]
                        assert not _can_directly_replace_with_src_expr, (s, low, high, existing_part)
                        assert not can_directly_replace_with_src_expr, (s, low, high, existing_part)
                        assert isinstance(existing_part, RtlSignal), (s, low, high, existing_part)
                    else:
                        assert sp_i == split_i +1, (s, sp_i, split_i)
                        # get actual input signal
                        if src is None:
                            _src = None
                        else:
                            _src = src[sp - dst_offset:prev_sp - dst_offset]

                        part_indexes = (SLICE.from_py(slice(sp, prev_sp, -1)),)
                        _src = construct_tmp_dst_sig_for_slice(s, part_indexes, _src, True)

                        new_parts.append(_src)
                        new_parts_dict[part_key] = _src, can_directly_replace_with_src_expr

                        split_i += 1
                    _split_parts.append(part_key)
                    prev_sp = sp

                new_parts_dict[index_key] = _split_parts, False

            end = max(end, high)

        if end < split_point[-1]:
            # something unconnected at the end
            high, low = split_point[-1], end
            part_indexes = (SLICE.from_py(slice(high, low , -1)),)
            _src = construct_tmp_dst_sig_for_slice(s, part_indexes, None, True)
            new_parts.append(_src)
            index_key = ((high, low),)
            new_parts_dict[index_key] = _src, True

        # construct assignment of concatenation from all parts
        assert new_parts, (s, parts)
        s(Concat(*reversed(new_parts)))
        final_signal_parts[s] = new_parts_dict

    return final_signal_parts


@internal
def extract_part_drivers(netlist: "RtlNetlist"):
    """
    .. code-block:: verilog

        if (c0)
            s[0] <= x;
        if (c1)
            s[1] <= y;

    to

    .. code-block:: verilog

        wire s_0_tmp;
        wire s_1_tmp;
        assign s <= {s_1_tmp, s_0_tmp};
        if (c0)
            s_0_tmp <= x;
        if (c1)
            s_1_tmp <= y;

    """
    signal_parts = {}
    for stm in sorted(netlist.statements, key=HdlStatement_sort_key):
        for s, indexes, can_directly_replace_with_src_expr, src in find_independent_slice_drivers(stm):
            signal_parts.setdefault(s, []).append((indexes, can_directly_replace_with_src_expr, src))

    if not signal_parts:
        return

    final_signal_parts = resolve_final_parts_from_splitpoints_and_parts(signal_parts)
    for stm in sorted(netlist.statements, key=HdlStatement_sort_key):
        extract_part_drivers_stm(stm, final_signal_parts)
