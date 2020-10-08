from types import MethodType
from typing import Tuple, Set, Optional

from hwt.doc_markers import internal
from hwt.synthesizer.exceptions import IntfLvlConfErr
from hwt.synthesizer.hObjList import HObjList
from hwt.synthesizer.interfaceLevel.mainBases import UnitBase, InterfaceBase
from hwt.synthesizer.param import Param
from hdlConvertorAst.translate.common.name_scope import WithNameScope


@internal
def nameAvailabilityCheck(obj, propName, prop):
    """
    Check if not redefining property on obj
    """
    if getattr(obj, propName, None) is not None:
        raise IntfLvlConfErr("%r already has property %s old:%s new:%s" % 
                             (obj, propName, repr(getattr(obj, propName)), prop))


@internal
class MakeParamsShared(object):
    """
    All newly added interfaces and units will share all parametes with unit
    specified in constructor of this object.
    """

    def __init__(self, unit, exclude, prefix):
        self.unit = unit
        self.exclude = exclude
        self.prefix = prefix

    def __enter__(self):
        orig = self.unit._setAttrListener
        self.orig = orig
        exclude = self.exclude
        prefix = self.prefix

        def MakeParamsSharedWrap(self, iName, i):
            if isinstance(i, (InterfaceBase, UnitBase, HObjList)):
                i._updateParamsFrom(self, exclude=exclude, prefix=prefix)
            return orig(iName, i)

        self.unit._setAttrListener = MethodType(MakeParamsSharedWrap,
                                                self.unit)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.unit._setAttrListener = self.orig


@internal
class MakeClkRstAssociations(object):
    """
    All newly added interfaces will be associated with clk, rst
    specified in constructor of this object.
    """

    def __init__(self, unit, clk=None, rst=None):
        self.unit = unit
        self.clk = clk
        self.rst = rst

    def __enter__(self):
        orig = self.unit._setAttrListener
        self.orig = orig
        clk = self.clk
        rst = self.rst

        def MakeClkRstAssociationsWrap(self, iName, i):
            if isinstance(i, (InterfaceBase, HObjList)):
                i._make_association(clk=clk, rst=rst)
            return orig(iName, i)

        self.unit._setAttrListener = MethodType(MakeClkRstAssociationsWrap,
                                                self.unit)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.unit._setAttrListener = self.orig


class PropDeclrCollector(object):
    """
    Class which manages the registration of components and interfaces
    in specified elaboration phases.

    It uses __setattr__ listeners to detect new properties and then calls
    a litener function to process the registration. 

    Used for Unit, Interface classes to detect and load interfaces and components.
    """

    def _config(self) -> None:
        """
        Configure object parameters

        * setup all parameters on this object,
          use Param class instances to allow use of parameter inheritance
        * called in __init__ of class
        """
        pass

    def _declr(self) -> None:
        """
        declarations

        * do all declarations of externally accessible objects there (Interfaces)
        * _declr method is called after _config
        * if this object is Unit all interfaces are threated as externally accessible interfaces
          if this object is Interface instance all subinterfaces are loaded as well
        """
        pass

    def _impl(self) -> None:
        """
        implementations

        * implement functionality of componnent there
        * called after _declr
        """
        pass

    @internal
    def __setattr__(self, attr, value) -> None:
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
            self._params = []

        self._setAttrListener = self._paramCollector
        self._config()
        self._setAttrListener = None

    @internal
    def _registerParameter(self, pName, parameter: Param) -> None:
        """
        Register Param object on interface level object
        """
        nameAvailabilityCheck(self, pName, parameter)
        # resolve name in this scope
        assert parameter._name is None, (
            "Param object is already assigned to %r.%s"
            % (parameter.unit, parameter._name))
        # add name in this scope
        parameter._name = pName
        parameter._parent = self

        self._params.append(parameter)

    def _paramsShared(self,
                      exclude: Optional[Tuple[Set[str], Set[str]]]=None,
                      prefix="") -> MakeParamsShared:
        """
        Auto-propagate params by name to child components and interfaces
        Usage:

        .. code-block:: python

            with self._paramsShared():
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
                self.myAxi = AxiStrem()
                # this interface is associated with myClk and myRst
                # simulation agents and component builders will use them


        :param exclude: params which should not be shared
        """
        return MakeClkRstAssociations(self, clk, rst)

    def _updateParamsFrom(self,
                          otherObj: "PropDeclrCollector",
                          updater,
                          exclude: Optional[Tuple[Set[str], Set[str]]],
                          prefix: str) -> "PropDeclrCollector":
        """
        Update all parameters which are defined on self from otherObj

        :param otherObj: other object which Param instances should be updated
        :param updater: updater function(self, myParameter,
                                         onOtherParameterName, otherParameter)
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

        for myP in self._params:
            if exclude is not None and myP._name in exclude_dst:
                excluded_dst.add(myP._name)
                continue
            pPName = prefix + myP._name
            try:
                otherP = getattr(otherObj, pPName)
                # if not isinstance(otherP, Param):
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
    def _registerUnit(self, uName, unit):
        """
        Register unit object on interface level object
        """
        nameAvailabilityCheck(self, uName, unit)
        assert unit._parent is None
        unit._parent = self
        unit._name = uName
        self._units.append(unit)

    @internal
    def _registerInterface(self, iName, intf, isPrivate=False):
        """
        Register interface object on interface level object
        """
        nameAvailabilityCheck(self, iName, intf)
        assert intf._parent is None
        intf._parent = self
        intf._name = iName
        intf._ctx = self._ctx

        # _setAsExtern() not used because _interfaces are not intitialized yet
        if isPrivate:
            self._private_interfaces.append(intf)
            intf._isExtern = False
        else:
            self._interfaces.append(intf)
            intf._isExtern = True

    @internal
    def _declrCollector(self, name, prop):
        if name in ("_associatedClk", "_associatedRst"):
            object.__setattr__(self, name, prop)
            return prop

        if isinstance(prop, InterfaceBase):
            self._registerInterface(name, prop)
        elif isinstance(prop, UnitBase):
            self._registerUnit(name, prop)
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
    def _registerUnitInImpl(self, uName, u):
        """
        :attention: unit has to be parametrized before it is registered
            (some components can change interface by parametrization)
        """
        self._registerUnit(uName, u)
        u._loadDeclarations()
        sm = self._store_manager
        with WithNameScope(sm, sm.name_scope.parent):
            self._lazy_loaded.extend(u._to_rtl(
                self._target_platform, self._store_manager))
        u._signalsForSubUnitEntity(self._ctx, "sig_" + uName)

    @internal
    def _registerIntfInImpl(self, iName, i):
        """
        Register interface in implementation phase
        """
        raise NotImplementedError()

    @internal
    def _paramCollector(self, pName, prop):
        if isinstance(prop, Param):
            self._registerParameter(pName, prop)
            return prop._initval
        else:
            return prop

    @internal
    def _implCollector(self, name, prop):
        """
        Hangle property definitions in _impl phase
        """
        if isinstance(prop, InterfaceBase):
            self._registerIntfInImpl(name, prop)
        elif isinstance(prop, UnitBase):
            self._registerUnitInImpl(name, prop)
        elif isinstance(prop, HObjList):
            self._registerArray(name, prop)
        return prop
