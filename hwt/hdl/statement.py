from itertools import chain
from typing import List, Tuple, Union, Optional

from hwt.doc_markers import internal
from hwt.hdl.hdlObject import HdlObject
from hwt.hdl.sensitivityCtx import SensitivityCtx
from hwt.pyUtils.arrayQuery import flatten
from hwt.pyUtils.uniqList import UniqList
from hwt.synthesizer.rtlLevel.mainBases import RtlSignalBase


class HwtSyntaxError(Exception):
    pass


class HdlStatement(HdlObject):
    """
    :ivar ~._event_dependent_from_branch: index of code branch if statement is event (clk) dependent else None
    :ivar ~.parentStm: parent instance of HdlStatement or None
    :ivar ~._inputs: UniqList of input signals for this statement
    :ivar ~._outputs: UniqList of output signals for this statement
    :ivar ~._sensitivity: UniqList of input signals
        or (rising/falling) operator
    :ivar ~._enclosed_for: set of outputs for which this statement is enclosed
        (for which there is not any unused branch)
    :ivar ~.rank: number of used branches in statement, used as pre-filter
        for statement comparing
    """

    def __init__(self, parentStm:Optional["HdlStatement"]=None, sensitivity:Optional[UniqList]=None,
                 event_dependent_from_branch:Optional[int]=None):
        assert event_dependent_from_branch is None or isinstance(event_dependent_from_branch, int), event_dependent_from_branch
        self._event_dependent_from_branch = event_dependent_from_branch
        self.parentStm = parentStm
        self._inputs = UniqList()
        self._outputs = UniqList()
        self._enclosed_for = None

        self._sensitivity = sensitivity
        self.rank = 0

    @internal
    def _clean_signal_meta(self):
        """
        Clean informations about enclosure for outputs and sensitivity
        of this statement
        """
        self._enclosed_for = None
        self._sensitivity = None
        for stm in self._iter_stms():
            stm._clean_signal_meta()

    @internal
    def _collect_io(self) -> None:
        """
        Collect inputs/outputs from all child statements
        to :py:attr:`~_input` / :py:attr:`_output` attribute on this object
        """
        in_add = self._inputs.extend
        out_add = self._outputs.extend

        for stm in self._iter_stms():
            in_add(stm._inputs)
            out_add(stm._outputs)

    @internal
    def _collect_inputs(self) -> None:
        """
        Collect inputs from all child statements
        to :py:attr:`~_input` attribute on this object
        """
        in_add = self._inputs.extend

        for stm in self._iter_stms():
            in_add(stm._inputs)

    @internal
    def _collect_outputs(self) -> None:
        """
        Collect inputs from all child statements
        to :py:attr:`_output` attribute on this object
        """

        out_add = self._outputs.extend

        for stm in self._iter_stms():
            out_add(stm._outputs)

    @internal
    def _cut_off_drivers_of(self, sig: RtlSignalBase) -> Union[None, "HdlStatement", List["HdlStatement"]]:
        """
        Cut all logic from statements which drives signal sig.

        :param sig: signal which drivers should be removed
        :return: A statement or statement list which was cut off from the original statement
        """
        raise NotImplementedError("This is an abstract method and it should be implemented in child class")

    @internal
    def _cut_off_drivers_of_regenerate_io(self, cut_off_sig: RtlSignalBase, cut_of_smt: "HdlStatement"):
        """
        Update _inputs/_outputs after some part of statement was cut of

        :param cut_off_sig: a signal which driver is a cut_of_stm
        :param cut_of_smt: the statement wich was cut off from original statement (selected by cut_off_sig)
        """
        # update io of this
        self._outputs.remove(cut_off_sig)
        if cut_of_smt._inputs:
            # update inputs on this
            self._inputs.clear()
            self._collect_inputs()
            if self.parentStm is None:
                for i in cut_of_smt._inputs:
                    if i not in self._inputs:
                        i.endpoints.remove(self)

        if self.parentStm is None:
            cut_off_sig.drivers.append(cut_of_smt)

    @internal
    def _discover_enclosure(self) -> None:
        """
        Discover all outputs for which is this statement enclosed _enclosed_for property
        (has driver in all code branches)
        """
        raise NotImplementedError("This method should be implemented"
                                  " on class of statement", self.__class__, self)

    @internal
    def _discover_sensitivity(self, seen: set) -> None:
        """
        discover all sensitivity signals and store them to _sensitivity property
        """
        raise NotImplementedError("This method should be implemented"
                                  " on class of statement", self.__class__, self)

    @internal
    def _get_rtl_context(self):
        """
        get RtlNetlist context from signals
        """
        for sig in chain(self._inputs, self._outputs):
            if sig.ctx:
                return sig.ctx
            else:
                # Param instances does not have context
                continue
        raise HwtSyntaxError(
            "Statement does not have any signal in any context,"
            " it should have at least some output or should be alreary optimized out", self)

    def _iter_stms(self):
        """
        :return: iterator over all children statements
        """
        raise NotImplementedError("This method should be implemented"
                                  " on class of statement", self.__class__,
                                  self)

    @internal
    def _on_reduce(self, self_reduced: bool, io_changed: bool,
                   result_statements: List["HdlStatement"]) -> None:
        """
        Update signal IO after reduce attempt

        :param self_reduced: if True this object was reduced
        :param io_changed: if True IO of this object may changed
            and has to be updated
        :param result_statements: list of statements which are result
            of reduce operation on this statement
        """

        parentStm = self.parentStm
        if self_reduced:
            was_top = parentStm is None
            # update signal drivers/endpoints
            if was_top:
                # disconnect self from signals
                ctx = self._get_rtl_context()
                ctx.statements.remove(self)
                ctx.statements.update(result_statements)

                for i in self._inputs:
                    i.endpoints.discard(self)
                for o in self._outputs:
                    o.drivers.remove(self)

            for stm in result_statements:
                stm.parentStm = parentStm
                if parentStm is None:
                    # connect signals to child statements
                    for inp in stm._inputs:
                        inp.endpoints.append(stm)
                    for outp in stm._outputs:
                        outp.drivers.append(stm)
        else:
            # parent has to update it's inputs/outputs
            if io_changed:
                self._inputs = UniqList()
                self._outputs = UniqList()
                self._collect_io()

    @internal
    def _on_merge(self, other):
        """
        After merging statements update IO, sensitivity and context

        :attention: rank is not updated
        """
        self._inputs.extend(other._inputs)
        self._outputs.extend(other._outputs)

        if self._sensitivity is not None:
            self._sensitivity.extend(other._sensitivity)
        else:
            assert other._sensitivity is None

        if self._enclosed_for is not None:
            self._enclosed_for.update(other._enclosed_for)
        else:
            assert other._enclosed_for is None

        other_was_top = other.parentStm is None
        if other_was_top:
            other._get_rtl_context().statements.remove(other)
            for s in other._inputs:
                s.endpoints.discard(other)
                s.endpoints.append(self)

            for s in other._outputs:
                s.drivers.discard(other)
                s.drivers.append(self)

    @internal
    def _try_reduce(self) -> Tuple[List["HdlStatement"], bool]:
        raise NotImplementedError("This method should be implemented"
                                  " on class of statement", self.__class__,
                                  self)

    def _is_enclosed(self) -> bool:
        """
        :return: True if every branch in statement assignas to all output signals else False
        """
        return len(self._outputs) == len(self._enclosed_for)

    @internal
    def _is_mergable(self, other: "HdlStatement") -> bool:
        if self is other:
            raise ValueError("Can not merge statement with itself")
        else:
            raise NotImplementedError("This method should be implemented"
                                      " on class of statement", self.__class__,
                                      self)

    @internal
    def _on_parent_event_dependent(self):
        """
        After parent statement become event dependent
        propagate event dependency flag to child statements
        """
        if self._event_dependent_from_branch != 0:
            self._event_dependent_from_branch = 0
            for stm in self._iter_stms():
                stm._on_parent_event_dependent()

    @internal
    def _set_parent_stm(self, parentStm: "HdlStatement"):
        """
        Assign parent statement and propagate dependency flags if necessary
        """
        was_top = self.parentStm is None
        self.parentStm = parentStm
        if self._event_dependent_from_branch is None\
                and parentStm._event_dependent_from_branch is not None:
            self._on_parent_event_dependent()

        topStatement = parentStm
        parents = []
        while True:
            parents.append(topStatement)
            if topStatement.parentStm is None:
                break
            topStatement = topStatement.parentStm

        if was_top:
            for inp in self._inputs:
                inp.endpoints.discard(self)
                inp.endpoints.append(topStatement)
                for p in parents:
                    p._inputs.append(inp)

            for outp in self._outputs:
                outp.drivers.discard(self)
                outp.drivers.append(topStatement)
                for p in parents:
                    p._outputs.append(outp)

            ctx = self._get_rtl_context()
            ctx.statements.discard(self)

        parentStm.rank += self.rank

    @internal
    def _register_stements(self, statements: List["HdlStatement"],
                           target: List["HdlStatement"]):
        """
        Append statements to this container
        """
        for stm in flatten(statements):
            assert stm.parentStm is None, (
                "HdlStatement instance has to have only a single parent", stm)
            stm._set_parent_stm(self)
            target.append(stm)

    def isSame(self, other: "HdlStatement") -> bool:
        """
        :return: True if other has same meaning as self
        """
        raise NotImplementedError("This method should be implemented in child class", self.__class__, self)

    @internal
    def _destroy(self):
        """
        Disconnect this statement from signals and delete it from RtlNetlist context

        :attention: signal endpoints/drivers will be altered
            that means they can not be used for iteration
        """
        for i in self._inputs:
            i.endpoints.discard(self)

        if self.parentStm is None:
            ctx = self._get_rtl_context()
            for o in self._outputs:
                o.drivers.remove(self)

            ctx.statements.remove(self)
            self.parentStm = None

    @internal
    def _replace_input(self, toReplace: RtlSignalBase,
                       replacement: RtlSignalBase) -> None:
        """
        Replace input signal with another

        :note: sensitivity/endoints are actualized
        """
        raise NotImplementedError("This method should be implemented in child class", self.__class__, self)

    @internal
    def _replace_input_update_sensitivity_and_enclosure(
            self,
            toReplace: RtlSignalBase,
            replacement: RtlSignalBase):
        if self._sensitivity is not None:
            if self._sensitivity.discard(toReplace):
                self._sensitivity.add(replacement)

        if self._enclosed_for is not None:
            if self._enclosed_for.discard(toReplace):
                self._enclosed_for.add(replacement)

    @internal
    def _replace_child_statement(self, stm: "HdlStatement",
                                 replacement: List["HdlStatement"],
                                 update_io: bool) -> None:
        """
        Replace a child statement with a list of other statements

        :attention: original statement is destroyed and entirely removed from circuit
        :note: sensitivity/endoints are actualized
        """
        raise NotImplementedError("This method should be implemented in child class", self.__class__, self)

