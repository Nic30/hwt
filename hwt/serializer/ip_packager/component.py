from time import time

from hwt.pyUtils.arrayQuery import arr_any
from hwt.serializer.ip_packager.busInterface import BusInterface
from hwt.serializer.ip_packager.helpers import appendSpiElem, \
    appendStrElements, mkSpiElm, ns, whereEndsWithExt, whereEndsWithExts
from hwt.serializer.ip_packager.model import Model
from hwt.serializer.ip_packager.otherXmlObjs import VendorExtensions,\
    FileSet, File, Parameter, Value
from hwt.serializer.ip_packager.port import Port
from hwt.synthesizer.interfaceLevel.interfaceUtils.utils import NotSpecified
import xml.etree.ElementTree as etree
from os.path import basename
from itertools import islice


vhdl_syn_fileSetName = "xilinx_vhdlsynthesis_view_fileset"
vhdl_sim_fileSetName = "xilinx_vhdlbehavioralsimulation_view_fileset"
tcl_fileSetName = "xilinx_xpgui_view_fileset"


def tcl_comment(s):
    return "# %s" % s


def tcl_set_module_property(name: str, value, escapeStr=True):
    if escapeStr and isinstance(value, str):
        value = '"%s"' % value
    elif isinstance(value, bool):
        value = str(value).lower()
    else:
        value = "%r" % value

    return "set_module_property %s %s" % (name, value)


def tcl_add_fileset_file(filename: str):
    """
    :param filename: relative filename with .vhdl or .v

    :return: add_fileset_file command string
    """
    if filename.endswith(".vhd"):
        t = "VHDL"
    elif filename.endswith(".v") or filename.endswith(".sv"):
        t = "VERILOG"
    else:
        raise NotImplementedError(
            "Can not resolve type of file by extension", filename)
    name = basename(filename)

    return "add_fileset_file %s %s PATH %s" % (name, t, filename)


class Component():
    """
    Containers of informations about IP core

    :attention: Xilinx xml is element position dependent
    """
    _strValues = ["vendor", "library", "name", "version", "description"]
    # _iterableValues = ["fileSets", "parameters" ]

    def __init__(self):
        self.vendor = ''
        self.library = ''
        self.name = ""
        self.version = "1.0"
        self.busInterfaces = []
        self.model = Model(vhdl_syn_fileSetName,
                           vhdl_sim_fileSetName, tcl_fileSetName)
        self.fileSets = []
        self.description = ""
        self.parameters = []
        self.vendorExtensions = VendorExtensions()
        self._files = []
        self._topUnit = None

    # @classmethod
    # def load(cls, xmlStr):
    #    self = cls()
    #    for prefix, uri in ns.items():
    #        etree.register_namespace(prefix, uri)
    #    self.root = etree.fromstring(xmlStr)
    #    self.name = findS(self.root, "name").text
    #
    #    intf = findS(self.root, "busInterfaces")
    #    self.interfaces = {}
    #    for i in intf:
    #        i = BusInterface.fromElem(i)
    #        if i.name in self.interfaces.keys():
    #            raise Exception("Multiple interfaces with same name")
    #        self.interfaces[i.name] = i
    #    self.model = Model.fromElem(findS(self.root, "model"))
    #
    #    return self

    def _xmlFileSets(self, componentElem):
        def fileSetFromFiles(name, files):
            fileSet = FileSet()
            fileSet.name = name
            for fn in files:
                f = File.fromFileName(fn)
                fileSet.files.append(f)
            return fileSet
        filesets = appendSpiElem(componentElem, "fileSets")
        hdlExtensions = [".vhd", 'v']

        hdl_fs = fileSetFromFiles(vhdl_syn_fileSetName,
                                  whereEndsWithExts(self._files, hdlExtensions))
        hdl_sim_fs = fileSetFromFiles(vhdl_sim_fileSetName,
                                      whereEndsWithExts(self._files, hdlExtensions))
        tclFileSet = fileSetFromFiles(tcl_fileSetName,
                                      whereEndsWithExt(self._files, ".tcl"))
        for fs in [hdl_fs, hdl_sim_fs, tclFileSet]:
            filesets.append(fs.asElem())

    def _xmlParameters(self, compElem):
        parameters = appendSpiElem(compElem, "parameters")
        for p in self.parameters:
            parameters.append(p.asElem())

    def xml(self):
        # Vivado 2015.2 bug - order of all elements is NOT optional
        for prefix, uri in ns.items():
            etree.register_namespace(prefix, uri)
        c = mkSpiElm("component")
        appendStrElements(c, self, self._strValues[:-1])
        if arr_any(self.busInterfaces, lambda intf: hasattr(intf, "_bi")):
            bi = appendSpiElem(c, "busInterfaces")
            for intf in self.busInterfaces:  # for all interfaces which have bus interface class
                if hasattr(intf, "_bi"):
                    bi.append(intf._bi.asElem())

        c.append(self.model.asElem())
        self._xmlFileSets(c)

        appendStrElements(c, self, [self._strValues[-1]])
        self._xmlParameters(c)
        c.append(self.vendorExtensions.asElem(
            self.name + "_v" + self.version, revision=str(int(time()))))

        return c

    def asignTopUnit(self, unit):
        """
        Set hwt unit as template for component
        """
        self._topUnit = unit
        self.name = unit._name
        self.model.addDefaultViews(self._topUnit)
        for p in self._topUnit._entity.ports:
            self.model.ports.append(Port._entPort2CompPort(unit._entity, p))

        for intf in unit._interfaces:
            if intf._isExtern:
                self.busInterfaces.append(intf)

        self.busInterfaces.sort(key=lambda x: x._name)
        for intf in self.busInterfaces:
            biClass = None
            try:
                biClass = intf._getIpCoreIntfClass()
            except NotSpecified:
                pass
            if biClass is not None:
                bi = BusInterface.fromBiClass(intf, biClass)
                intf._bi = bi
                bi.busType.postProcess(
                    self, self._topUnit, self.busInterfaces, intf)

        # generate component parameters
        compNameParam = Parameter()
        compNameParam.name = "Component_Name"
        compNameParam.value = Value()
        v = compNameParam.value
        v.id = "PARAM_VALUE.Component_Name"
        v.resolve = "user"
        v.text = self.name
        self.parameters.append(compNameParam)
        # generic as parameters
        for g in self._topUnit._entity.generics:
            p = Parameter()
            p.name = g.name
            p.value = Value.fromGeneric("PARAM_VALUE.", g, Value.RESOLVE_USER)
            self.parameters.append(p)

        # for bi in self.busInterfaces:
        #    bi.name = trimUnderscores(bi.name)
        #    for p in bi.parameters:
        #        p.name = removeUndescores_witSep(p.name, ".")
        #        p.value.id = removeUndescores_witSep(p.value.id , ".")
        #        p.value.text = removeUndescores_witSep(p.value.text , ".")

    def quartus_tcl(self, quartus_version="16.1"):
        buff = [
            tcl_comment("module properties"),
            "package require -exact qsys %s" % quartus_version,
            tcl_set_module_property("DESCRIPTION", self.description),
            tcl_set_module_property("NAME", self.name),
            tcl_set_module_property("VERSION", self.version),
            tcl_set_module_property("INTERNAL", False),
            tcl_set_module_property("OPAQUE_ADDRESS_MAP", True),
            tcl_set_module_property("GROUP", self.library),
            tcl_set_module_property("AUTHOR", self.vendor),
            tcl_set_module_property("DISPLAY_NAME", self.name),
            tcl_set_module_property("INSTANTIATE_IN_SYSTEM_MODULE", True),
            tcl_set_module_property("EDITABLE", True),
            tcl_set_module_property("REPORT_TO_TALKBACK", False),
            tcl_set_module_property("ALLOW_GREYBOX_GENERATION", False),
            tcl_set_module_property("REPORT_HIERARCHY", False),
        ]

        buff.extend([
            'add_fileset QUARTUS_SYNTH QUARTUS_SYNTH "" ""',
            'set_fileset_property QUARTUS_SYNTH TOP_LEVEL %s' % self.name,
            "set_fileset_property QUARTUS_SYNTH ENABLE_RELATIVE_INCLUDE_PATHS false"
            "set_fileset_property QUARTUS_SYNTH ENABLE_FILE_OVERWRITE_MODE false"
        ])
        for f in self._files:
            if not f.endswith(".tcl"):
                s = tcl_add_fileset_file(f)
                buff.append(s)

        buff.append(tcl_comment("params"))
        # first is name of this component
        for p in islice(self.parameters, 1, None):
            p.asQuartusTcl(buff, quartus_version)

        buff.append(tcl_comment("interfaces"))
        for intf in self.busInterfaces:
            # for all interfaces which have bus interface class
            if hasattr(intf, "_bi"):
                bi = intf._bi
                bi.busType.asQuartusTcl(buff, quartus_version,
                                        self, self._topUnit,
                                        self.busInterfaces, intf)
                buff.append("")
        return "\n".join(buff)