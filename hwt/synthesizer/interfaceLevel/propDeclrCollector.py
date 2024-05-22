from types import MethodType
from typing import Tuple, Set, Optional, Callable

from hwt.doc_markers import internal
from hwt.synthesizer.exceptions import IntfLvlConfErr
from hwt.hObjList import HObjList
from hwt.mainBases import HwModuleBase, HwIOBase
from hwt.hwParam import HwParam
from hdlConvertorAst.translate.common.name_scope import WithNameScope


@internal
def nameAvailabilityCheck(obj, propName, prop):
    """
    Check if not redefining property on obj
    but allow to cast current property to a parameter
    """
    cur = getattr(obj, propName, None)
    if cur is not None and (not isinstance(prop, HwParam) or cur is not prop._initval):
        p = getattr(obj, propName)
        raise IntfLvlConfErr(f"{obj} already has property {propName:s} old:{p} new:{prop}")


@internal
class MakeParamsShared(object):
    """
    All newly added interfaces and units will share all parametes with unit
    specified in constructor of this object.
    """

    def __init__(self, module: "HwModule", exclude:Optional[Tuple[Set[str], Set[str]]], prefix:str):
        self.module = module
        self.exclude = exclude
        self.prefix = prefix

    def __enter__(self):
        orig = self.module._setAttrListener
        self.orig = orig
        exclude = self.exclude
        prefix = self.prefix

        def MakeParamsSharedWrap(self, iName, i):
            if isinstance(i, (HwIOBase, HwModuleBase, HObjList)):
                i._updateParamsFrom(self, exclude=exclude, prefix=prefix)
            return orig(iName, i)

        self.module._setAttrListener = MethodType(MakeParamsSharedWrap,
                                                self.module)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.module._setAttrListener = self.orig


@internal
class MakeClkRstAssociations(object):
    """
    All newly added interfaces will be associated with clk, rst
    specified in constructor of this object.
    """

    def __init__(self, module: "HwModule", clk=None, rst=None):
        self.module = module
        self.clk = clk
        self.rst = rst

    def __enter__(self):
        orig = self.module._setAttrListener
        self.orig = orig
        clk = self.clk
        rst = self.rst

        def MakeClkRstAssociationsWrap(self, iName, i):
            if isinstance(i, (HwIOBase, HObjList)):
                i._make_association(clk=clk, rst=rst)
            return orig(iName, i)

        self.module._setAttrListener = MethodType(MakeClkRstAssociationsWrap,
                                                  self.module)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.module._setAttrListener = self.orig


class PropDeclrCollector(object):
    """
    Class which manages the registration of components and interfaces
    in specified elaboration phases.

    It uses __setattr__ listeners to detect new properties and then calls
    a litener function to process the registration.

    Used for HwModule, HwIO classes to detect and load interfaces and components.
    """

    def _config(self) -> None:
        """
        Configure object parameters

        * setup all parameters on this object,
          use HwParam class instances to allow use of parameter inheritance
        * called in __init__ of class
        """
        pass

    def _declr(self) -> None:
        """
        In this function user should specify the declaration of interfaces for communication with outside word.
        It is also better to declare sub components there as it allows for better parallelization during the build.

        * _declr method is called after _config
        * if this object is :class:`hwt.hwModule.HwModule` all interfaces are treated as externally accessible interfaces
          if this object is HwIO instance all subinterfaces are loaded as well
        """
        pass

    def _impl(self) -> None:
        """
        Implementation - construct main body of the component in this function.

        * called after _declr
        """
        pass

    @internal
    def __setattr__(self, attr:str, value) -> None:
        """setattr with listener injector"""
        try:
            saListerner = self._setAttrListener
        except AttributeError:
            super().__setattr__(attr, value)
            return

        if saListerner:
            value = saListerner(attr, value)
        super().__setattr__(attr, value)

    # configuration phase
    @internal
    def _loadConfig(self) -> None:
        """
        Load params in _config()
        """
        if not hasattr(self, '_params'):
            self._hwParams = []

        self._setAttrListener = self._paramCollector
        self._config()
        self._setAttrListener = None

    @internal
    def _registerParameter(self, pName:str, parameter: HwParam) -> None:
        """
        Register HwParam object on interface level object
        """
        nameAvailabilityCheck(self, pName, parameter)
        # resolve name in this scope
        assert parameter._name is None, (
            "HwParam object is already assigned to %r.%s"
            % (parameter.module, parameter._name))
        # add name in this scope
        parameter._name = pName
        parameter._parent = self

        self._hwParams.append(parameter)

    def _hwParamsShared(self,
                      exclude: Optional[Tuple[Set[str], Set[str]]]=None,
                      prefix="") -> MakeParamsShared:
        """
        Auto-propagate params by name to child components and interfaces
        Usage:

        .. code-block:: python

            with self._hwParamsShared():
                # your interfaces and unit which should share all params with "self" there

        :param exclude: tuple (src param names to exclude, dst param names to exclude)
        :param prefix: prefix which should be added to name of child parameters
            before parameter name matching
        """
        return MakeParamsShared(self, exclude=exclude, prefix=prefix)

    def _make_association(self, clk=None, rst=None) -> None:
        """
        Associate this object with specified clk/rst
        """
        if clk is not None:
            assert self._associatedClk is None, ("Already associated with clock", self._associatedClk)
            self._associatedClk = clk

        if rst is not None:
            assert self._associatedRst is None, ("Already associated with reset", self._associatedRst)
            self._associatedRst = rst

    def _associated(self, clk=None, rst=None) -> MakeClkRstAssociations:
        """
        associate newly added interfaces to "self" with selected clk, rst
        (if interface is not associated agents try to find clk/rst by _getAssociatedClk/_getAssociatedRst
        which will search for any clk/rst on parent recursively)
        Usage:

        .. code-block:: python

            with self._associated(clk=self.myClk, rst=self.myRst):
                self.myAxi = Axi4Stream()
                # this interface is associated with myClk and myRst
                # simulation agents and component builders will use them


        :param exclude: params which should not be shared
        """
        return MakeClkRstAssociations(self, clk, rst)

    def _updateParamsFrom(self,
                          otherObj: "PropDeclrCollector",
                          updater: Callable[["PropDeclrCollector", HwParam, HwParam], None],
                          exclude: Optional[Tuple[Set[str], Set[str]]],
                          prefix: str) -> "PropDeclrCollector":
        """
        Update all parameters which are defined on self from otherObj

        :param otherObj: other object which HwParam instances should be updated
        :param updater: updater function(self, myParameter, otherParameter)
        :param exclude: tuple of set of param names for src and dst which
                        which should be excluded
        :param prefix: prefix which should be added to name of paramters
                       of this object before matching parameter name on parent
        """
        excluded_src = set()
        excluded_dst = set()
        if exclude is not None:
            exclude_src = set(exclude[0])
            exclude_dst = set(exclude[1])

        for myP in self._hwParams:
            if exclude is not None and myP._name in exclude_dst:
                excluded_dst.add(myP._name)
                continue
            pPName = prefix + myP._name
            try:
                otherP = getattr(otherObj, pPName)
                # if not isinstance(otherP, HwParam):
                #     continue
            except AttributeError:
                continue

            if exclude is not None and pPName in exclude_src:
                excluded_src.add(pPName)
                continue
            updater(self, myP, otherP)

        if exclude is not None:
            # assert that what should be excluded really exists
            assert exclude_src == excluded_src, (exclude_src, excluded_src)
            assert exclude_dst == excluded_dst, (exclude_dst == excluded_dst)
        return self

    # declaration phase
    @internal
    def _registerSubmodule(self, mName:str, submodule:"HwModule"):
        """
        Register unit object on interface level object
        """
        nameAvailabilityCheck(self, mName, submodule)
        assert submodule._parent is None
        submodule._parent = self
        submodule._name = mName
        self._subHwModules.append(submodule)

    @internal
    def _registerHwIO(self, hwIOName, hwIO, isPrivate=False):
        """
        Register HwIO object on interface level object
        """
        nameAvailabilityCheck(self, hwIOName, hwIO)
        assert hwIO._parent is None
        hwIO._parent = self
        hwIO._name = hwIOName
        hwIO._ctx = self._ctx

        # _setAsExtern() not used because _hwIOs are not initialized yet
        if isPrivate:
            self._private_hwIOs.append(hwIO)
            hwIO._isExtern = False
        else:
            self._hwIOs.append(hwIO)
            hwIO._isExtern = True

    @internal
    def _declrCollector(self, name: str, prop: object):
        if name in ("_associatedClk", "_associatedRst"):
            object.__setattr__(self, name, prop)
            return prop

        if isinstance(prop, HwIOBase):
            self._registerHwIO(name, prop)
        elif isinstance(prop, HwModuleBase):
            self._registerSubmodule(name, prop)
        elif isinstance(prop, HObjList):
            self._registerArray(name, prop)
        return prop

    @internal
    def _registerArray(self, name, items: HObjList):
        """
        Register array of items on interface level object
        """
        items._parent = self
        items._name = name
        items._on_append = self._registerArray_append
        for i, item in enumerate(items):
            self._registerArray_append(items, item, i)

    @internal
    def _registerArray_append(self, h_obj_list: HObjList, item, index: int):
        """
        Register a single object in the list
        """
        setattr(self, "%s_%d" % (h_obj_list._name, index), item)

    # implementation phase
    @internal
    def _loadImpl(self):
        self._setAttrListener = self._implCollector
        self._impl()
        self._setAttrListener = None

    @internal
    def _registerSubmoduleInImpl(self, uName, u):
        """
        :attention: unit has to be parametrized before it is registered
            (some components can change interface by parametrization)
        """
        self._registerSubmodule(uName, u)
        u._loadDeclarations()
        sm = self._store_manager
        with WithNameScope(sm, sm.name_scope.parent):
            self._lazy_loaded.extend(u._to_rtl(
                self._target_platform, self._store_manager))
        u._signalsForSubHwModuleEntity(self._ctx, "sig_" + uName)

    @internal
    def _registerHwIOInImpl(self, hwIOName, i):
        """
        Register interface in implementation phase
        """
        raise NotImplementedError()

    @internal
    def _paramCollector(self, pName, prop):
        if isinstance(prop, HwParam):
            self._registerParameter(pName, prop)
            return prop._initval
        else:
            return prop

    @internal
    def _implCollector(self, name, prop):
        """
        Handle property definitions in _impl phase
        """
        if isinstance(prop, HwIOBase):
            if prop._parent is self:
                return prop
            self._registerHwIOInImpl(name, prop)
        elif isinstance(prop, HwModuleBase):
            if prop._parent is self:
                return prop
            self._registerSubmoduleInImpl(name, prop)
        elif isinstance(prop, HObjList):
            if prop._parent is self:
                return prop
            self._registerArray(name, prop)
        return prop
