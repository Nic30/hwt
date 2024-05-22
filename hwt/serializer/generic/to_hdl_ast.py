from copy import copy, deepcopy
from typing import Optional, List, Union

from hdlConvertorAst.hdlAst import iHdlStatement, iHdlObj, HdlIdDef, \
    HdlValueId, HdlTypeType, iHdlExpr, HdlStmBlock, HdlStmIf, HdlStmCase, \
    HdlStmProcess, HdlStmAssign, HdlModuleDef, HdlModuleDec, \
    HdlCompInst, HdlEnumDef, HdlOp
from hdlConvertorAst.hdlAst._statements import ALL_STATEMENT_CLASSES
from hdlConvertorAst.to.basic_hdl_sim_model._main import ToBasicHdlSimModel
from hdlConvertorAst.translate.common.name_scope import NameScope, WithNameScope
from hdlConvertorAst.translate.verilog_to_basic_hdl_sim_model.utils import \
    hdl_index, hdl_map_asoc
from hwt.hdl.operator import HOperatorNode
from hwt.hdl.portItem import HdlPortItem
from hwt.hdl.statements.assignmentContainer import HdlAssignmentContainer
from hwt.hdl.statements.codeBlockContainer import HdlStmCodeBlockContainer
from hwt.hdl.statements.ifContainter import IfContainer
from hwt.hdl.statements.switchContainer import SwitchContainer
from hwt.hdl.types.array import HArray
from hwt.hdl.types.bits import HBits
from hwt.hdl.types.defs import STR, BOOL
from hwt.hdl.types.enum import HEnum
from hwt.hdl.types.float import HFloat
from hwt.hdl.types.hdlType import HdlType, MethodNotOverloaded
from hwt.hdl.types.slice import HSlice
from hwt.pyUtils.arrayQuery import arr_any
from hwt.serializer.exceptions import SerializerException
from hwt.serializer.exceptions import UnsupportedEventOpErr
from hwt.serializer.generic.tmpVarConstructor import TmpVarConstructor, \
    NoTmpVars
from hwt.serializer.generic.utils import HWT_TO_HDLCONVEROTR_DIRECTION, \
    TmpVarsSwap
from hwt.serializer.utils import HdlStatement_sort_key
from hwt.mainBases import RtlSignalBase
from hwt.hdl.const import HConst
from hwt.synthesizer.rtlLevel.rtlSignal import RtlSignal


class ToHdlAst():
    """
    Base class for translators which translates hwt AST to a HDL ast

    :ivar ~.name_scope: name scope for resolution of hdl names for objects
        and for name colision checking for newly generated objects
    :ivar ~.tmpVars: A object which is used to create a tmp variable in current scope.
        It is set if it is possible to create a tmp variable.
    :ivar ~.constCache: A ConstCache instance used o extract values as a constants.
    :type ~.constCache: Optional[ConstantCache]
    """
    # used to filter statems from other object by class without using
    # isisnstance
    ALL_STATEMENT_CLASSES = [*ALL_STATEMENT_CLASSES, HdlStmCodeBlockContainer]
    TMP_VAR_CONSTRUCTOR = TmpVarConstructor
    _keywords_dict = {}

    @classmethod
    def getBaseNameScope(cls):
        """
        Get root of name space
        """
        s = NameScope.make_top(False)
        s.update(cls._keywords_dict)
        return s

    def __init__(self, name_scope: Optional[NameScope]=None):
        if name_scope is None:
            name_scope = self.getBaseNameScope()
        self.name_scope = name_scope
        self.tmpVars = NoTmpVars()
        self.constCache = None

    def as_hdl(self, obj) -> iHdlObj:
        """
        Convert any object to HDL AST

        :param obj: object to convert
        """
        serFn = getattr(self, "as_hdl_" + obj.__class__.__name__, None)
        if serFn is not None:
            return serFn(obj)
        elif isinstance(obj, RtlSignalBase):
            return self.as_hdl_HdlSignalItem(obj)
        else:
            raise SerializerException(self,
                                      "Not implemented for obj of",
                                      obj.__class__, obj)

    def as_hdl_HdlType(self, typ: HdlType, declaration=False):
        try:
            return typ._as_hdl(self, declaration)
        except MethodNotOverloaded:
            pass

        if typ == STR:
            sFn = self.as_hdl_HdlType_str
        elif isinstance(typ, HBits):
            sFn = self.as_hdl_HdlType_bits
        elif isinstance(typ, HEnum):
            sFn = self.as_hdl_HdlType_enum
        elif isinstance(typ, HArray):
            sFn = self.as_hdl_HdlType_array
        elif isinstance(typ, HSlice):
            sFn = self.as_hdl_HdlType_slice
        elif isinstance(typ, HFloat):
            sFn = self.as_hdl_HdlType_float
        else:
            # [todo] better error msg
            raise NotImplementedError("type declaration is not implemented"
                                      " for type %s"
                                      % (HdlType.__repr__(typ)))

        return sFn(typ, declaration=declaration)

    def as_hdl_HdlType_array(self, typ: HArray, declaration=False):
        ns = self.name_scope
        if declaration:
            dec = HdlIdDef()
            dec.type = HdlTypeType
            if self.does_type_requires_extra_def(typ.element_t, ()):
                # problem there is that we do not have a list of already defined types
                # so we can not just declare an element type
                raise NotImplementedError(typ.element_t)

            dec.value = hdl_index(self.as_hdl_HdlType(typ.element_t, declaration=False),
                                  self.as_hdl_int(int(typ.size)))
            name = getattr(typ, "name", "arr_t_")
            dec.name = ns.checked_name(name, typ)
            return dec
        else:
            name = ns.get_object_name(typ)
            return HdlValueId(name, obj=typ)

    def as_hdl_HdlType_enum(self, typ: HEnum, declaration=False):
        ns = self.name_scope
        if declaration:
            e = HdlEnumDef()
            e.origin = typ
            e.name = ns.checked_name(typ.name, typ)
            e.values = [(ns.checked_name(n, getattr(typ, n)), None)
                        for n in typ._allValues]
            dec = HdlIdDef()
            dec.type = HdlTypeType
            dec.value = e
            dec.name = e.name
            return dec
        else:
            name = ns.get_object_name(typ)
            return HdlValueId(name, obj=None)

    def as_hdl_HdlType_slice(self, typ: HSlice, declaration=False):
        raise NotImplementedError(self)

    def as_hdl_If(self, *args, **kwargs) -> HdlStmIf:
        return self.as_hdl_IfContainer(*args, **kwargs)

    def as_hdl_cond(self, v, force_bool) -> iHdlExpr:
        if force_bool and v._dtype != BOOL:
            v = v._isOn()
        return self.as_hdl(v)

    def as_hdl_statements(self, stm_list) -> iHdlStatement:
        if stm_list is None:
            return None
        elif len(stm_list) == 1:
            return self.as_hdl(stm_list[0])
        else:
            b = HdlStmBlock()
            b.body = [self.as_hdl(s) for s in stm_list]
            return b

    def _as_hdl_HdlAssignmentContainer_auto_conversions(self, a: HdlAssignmentContainer):
        dst = a.dst
        src = a.src
        dst_indexes = a.indexes
        if a.indexes is not None:
            dst_indexes = [self.as_hdl(x) for x in dst_indexes]
            correct = True
        else:
            if dst._dtype == a.src._dtype:
                correct = True
            else:
                srcT = a.src._dtype
                dstT = dst._dtype
                correct = False
                if (isinstance(srcT, HBits) and
                        isinstance(dstT, HBits)):
                    bl0 = srcT.bit_length()
                    if bl0 == dstT.bit_length():
                        if bl0 == 1 and srcT.force_vector != dstT.force_vector:
                            if srcT.force_vector:
                                src = src[0]
                                correct = True
                            elif dstT.force_vector:
                                dst_indexes = [self.as_hdl_int(0), ]
                                correct = True
                        elif srcT.signed == dstT.signed:
                            correct = True

        if not correct:
            raise SerializerException((
                "%s <= %s  is not valid assignment\n"
                " because types are different (%r; %r) ") %
                (dst, src, dst._dtype, a.src._dtype))
        return dst, dst_indexes, self.as_hdl_Value(src)

    def as_hdl_HdlAssignmentContainer(self, a: HdlAssignmentContainer):
        dst, dst_indexes, src = self._as_hdl_HdlAssignmentContainer_auto_conversions(a)
        dst = self.as_hdl(dst)
        if dst_indexes:
            for i in dst_indexes:
                dst = hdl_index(dst, i)
        a = HdlStmAssign(src, dst)
        return a

    def as_hdl_IfContainer(self, ifc: IfContainer) -> HdlStmIf:
        try:
            cond = self.as_hdl_cond(ifc.cond, True)
        except UnsupportedEventOpErr:
            cond = None

        if cond is None:
            assert not ifc.elIfs
            assert not ifc.ifFalse
            return self.as_hdl_statements(ifc.ifTrue)

        elIfs = []
        ifTrue = self.as_hdl_statements(ifc.ifTrue)
        ifFalse = self.as_hdl_statements(ifc.ifFalse)

        for c, statements in ifc.elIfs:
            try:
                elIfs.append((self.as_hdl_cond(c, True),
                              self.as_hdl_statements(statements)))
            except UnsupportedEventOpErr:
                if len(ifc.elIfs) == 1 and not ifFalse:
                    # register expression is in valid format and this
                    # is just register with asynchronous reset or etc...
                    ifFalse = self.as_hdl_statements(statements)
                else:
                    raise

        i = HdlStmIf()
        i.cond = cond
        i.if_true = ifTrue
        i.elifs = elIfs
        i.if_false = ifFalse
        return i

    def as_hdl_Switch(self, *args, **kwargs) -> HdlStmCase:
        return self.as_hdl_SwitchContainer(*args, **kwargs)

    def as_hdl_FsmBuilder(self, *args, **kwargs) -> HdlStmCase:
        return self.as_hdl_SwitchContainer(*args, **kwargs)

    def as_hdl_SwitchContainer(self, sw: SwitchContainer) -> HdlStmCase:
        s = HdlStmCase()
        s.switch_on = self.as_hdl_cond(sw.switchOn, False)
        s.cases = cases = []
        for key, statements in sw.cases:
            key = self.as_hdl_Value(key)
            cases.append((key, self.as_hdl_statements(statements)))

        s.default = self.as_hdl_statements(sw.default)
        return s

    def as_hdl_PortConnection(self, o: HdlPortItem):
        assert isinstance(o, HdlPortItem), o
        if o.dst._dtype != o.src._dtype:
            raise SerializerException(
                f"Port map {o._name:s} is not valid (types does not match)  ({o.src._dtype}, {o.dst._dtype}) "
                f"{o.src} => {o.dst}"
            )

        intern, outer = o.getInternSig(), o.getOuterSig()
        intern_hdl = self.as_hdl_Value(intern)
        intern_hdl.obj = o
        outer_hdl = self.as_hdl_Value(outer)
        pm = hdl_map_asoc(intern_hdl, outer_hdl)
        return pm

    def as_hdl_HdlCompInst(self, o: HdlCompInst) -> HdlCompInst:
        new_o = copy(o)
        param_map = []
        for p in o.param_map:
            p: HdlIdDef
            assert isinstance(p, HdlIdDef), p
            pm = hdl_map_asoc(HdlValueId(p.name, obj=p), self.as_hdl(p.value))
            param_map.append(pm)
        new_o.param_map = param_map

        port_map = []
        for pi in o.port_map:
            pi: HdlPortItem
            pm = self.as_hdl_PortConnection(pi)
            port_map.append(pm)
        new_o.port_map = port_map
        return new_o

    def as_hdl_GenericItem(self, o: HdlIdDef):
        assert not self.does_type_requires_extra_def(o.type, tuple())
        return self.as_hdl_HdlModuleDef_variable(o, None, None, None, None, None)

    def as_hdl_HdlPortItem(self, o: HdlPortItem):
        var = HdlIdDef()
        var.direction = HWT_TO_HDLCONVEROTR_DIRECTION[o.direction]
        s = o.getInternSig()
        var.name = s._name
        var.origin = o
        var.type = o._dtype
        return self.as_hdl_HdlModuleDef_variable(var, (), None, None, None, None)

    def as_hdl_HdlModuleDec(self, o: HdlModuleDec):
        # :attention: name_scope should be already set to body of module
        # with WithNameScope(self, self.name_scope.get_child(o._name)):

        new_o = copy(o)

        # convert types, exprs
        new_o.params = [self.as_hdl_GenericItem(p) for p in o.params]
        new_o.ports = [self.as_hdl_HdlPortItem(p) for p in o.ports]

        return new_o

    def does_type_requires_extra_def(self, t: HdlType, other_types: list):
        try:
            return t._as_hdl_requires_def(self, other_types)
        except MethodNotOverloaded:
            pass
        return isinstance(t, (HEnum, HArray)) and t not in other_types

    def as_hdl_HdlModuleDef_variable(
            self, v, types, hdl_types, hdl_variables,
            processes, component_insts):
        t = v.type
        # if type requires extra definition
        if self.does_type_requires_extra_def(t, types):
            _t = self.as_hdl_HdlType(t, declaration=True)
            hdl_types.append(_t)
            types.add(t)

        return self.as_hdl_HdlSignalItem(v, declaration=True)

    def _as_hdl_HdlModuleDef(self, new_m: HdlModuleDef) -> HdlModuleDef:
        # with WithNameScope(self,
        # self.name_scope.get_child(o.module_name.val)):
        hdl_types, hdl_variables, processes, component_insts, others = \
            ToBasicHdlSimModel.split_HdlModuleDefObjs(self, new_m.objs)
        # [TODO] sorting not required as it should be done in _to_rtl()
        if len(hdl_variables) > 1:
            hdl_variables.sort(key=lambda x: (x.name, x.origin._instId))
        if len(processes) > 1:
            processes.sort(key=HdlStatement_sort_key)
        if len(component_insts) > 1:
            component_insts.sort(key=lambda x: x.name)

        types = set()

        extraVars = self.TMP_VAR_CONSTRUCTOR(self, self.name_scope)

        with TmpVarsSwap(self, extraVars):
            return self._as_hdl_HdlModuleDef_body(
                new_m, types, hdl_types, hdl_variables, extraVars,
                processes, component_insts, others)

    def _as_hdl_HdlModuleDef_body(
            self, new_m, types, hdl_types, hdl_variables,
            extraVars: TmpVarConstructor, processes: List[iHdlStatement],
            component_insts: List[HdlCompInst], others: List[Union[HdlOp, iHdlStatement]]):

        _hdl_variables = []
        for v in hdl_variables:
            new_v = self.as_hdl_HdlModuleDef_variable(
                v, types, hdl_types, hdl_variables,
                processes, component_insts)
            _hdl_variables.append(new_v)
        hdl_variables = _hdl_variables

        processes = [self.as_hdl_HdlStmCodeBlockContainer(p) for p in processes]

        component_insts = [self.as_hdl_HdlCompInst(c)
                           for c in component_insts]
        extraVars.sort_hdl_declarations_first()
        new_m.objs = hdl_types + hdl_variables + \
            extraVars.extraVarsHdl + component_insts + processes + others
        return new_m

    def as_hdl_HdlModuleDef(self, o: HdlModuleDef) -> HdlModuleDef:
        # :attention: name_scope should be already set to body of module
        new_m = copy(o)
        if o.dec is not None:
            new_m.dec = self.as_hdl_HdlModuleDec(o.dec)
        return self._as_hdl_HdlModuleDef(new_m)

    def has_to_be_process(self, proc: iHdlStatement):
        raise NotImplementedError(
            "This method should be overloaded in child class")

    def can_pop_process_wrap(self, statements, hasToBeVhdlProcess):
        raise NotImplementedError(
            "This method should be overloaded in child class")

    def as_hdl_HdlStmCodeBlockContainer(self, proc: HdlStmCodeBlockContainer) -> iHdlStatement:
        """
        Serialize HdlStmCodeBlockContainer objects as process if top statement
        """
        if isinstance(proc, ALL_STATEMENT_CLASSES):
            return proc
        assert proc.parentStm is None, proc
        body = proc.statements

        hasToBeVhdlProcess = self.has_to_be_process(proc)

        with WithNameScope(self, self.name_scope.level_push(proc.name)):
            tmpVars = self.TMP_VAR_CONSTRUCTOR(self, self.name_scope)
            with TmpVarsSwap(self, tmpVars):
                statements = [self.as_hdl(s) for s in body]

                hasToBeVhdlProcess |= bool(tmpVars.extraVarsHdl)

                if hasToBeVhdlProcess:
                    tmpVars.sort_hdl_declarations_first()
                    statements = tmpVars.extraVarsHdl + statements

                if self.can_pop_process_wrap(statements, hasToBeVhdlProcess):
                    return statements[0]
                else:
                    p = HdlStmProcess()
                    p.labels.append(proc.name)

                    if not statements:
                        pass  # no body
                    elif len(statements) == 1:
                        # body made of just a singe statement
                        p.body = statements[0]
                    else:
                        p.body = HdlStmBlock()
                        assert isinstance(statements, list)
                        p.body.body = statements
                    anyIsEventDependnt = arr_any(
                        proc._sensitivity, lambda s: isinstance(s, HOperatorNode))
                    p.sensitivity = sorted([
                        self.sensitivityListItem(s, anyIsEventDependnt)
                        for s in proc._sensitivity])
                    return p

    def _static_assert_false(self, msg:str):
        raise NotImplementedError("Should be implemented in child class")

    def _static_assert_symbol_eq(self, symbol_name:str, v):
        raise NotImplementedError("Should be implemented in child class")

    def _as_hdl_HdlModuleDef_param_asserts(self, new_m: HdlModuleDec) -> List[iHdlStatement]:
        return []

    def _as_hdl_HdlModuleDef_param_asserts_real(self, new_m: HdlModuleDec) -> List[iHdlStatement]:
        res = []
        for p in new_m.params:
            p: HdlIdDef
            if p.value is None:
                continue
            v = p.value
            if isinstance(v, (HConst, RtlSignal)):
                v = self.as_hdl(v)
            else:
                v = deepcopy(v)
            res.append(self._static_assert_symbol_eq(p.name, v))

        return res
