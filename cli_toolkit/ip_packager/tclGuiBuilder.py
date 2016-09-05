

class TclObj():
    pass

class GuiParam(TclObj):
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent

    def __str__(self):
        return 'ipgui::add_param $IPINST -name "%s" -parent ${%s}' % (self.name, self.parent.name)


class GuiPage(TclObj):
    __slots__ = ["name", 'parent']
    
    def __init__(self, name):
        self.name = name
        self.elements = []
        
    def param(self, name):
        p = GuiParam(name, self)
        self.elements.append(p)
        return p
    
    def __str__(self):
        params = []
        for n in self.__slots__:
            p = getattr(self, n, None)
            if p:
                if issubclass(p.__class__, TclObj):
                    s = '-%s ${%s}' % (n, p.name)
                else:
                    s = '-%s "%s"' % (n, p)
                params.append(s)
        page = 'set %s [ipgui::add_page $IPINST %s]' % (self.name, ' '.join(params))
        elements = '\n'.join(map(lambda x: str(x), self.elements))
        return '\n'.join([page, elements])
   
class GuiBuilder():
    
    def __init__(self):
        self.elements = []
    
    def page(self, name):
        p = GuiPage(name)
        self.elements.append(p)
        return p
        
    def asTcl(self):
        init_gui = TclFn("init_gui", ["IPINST"], self.elements)
        return str(init_gui)

class TclFn(TclObj):
    
    def __init__(self, name, params, body):
        self.name = name 
        self.params = params
        self.body = body
        
    def __str__(self):
        return "proc %s { %s } {\n %s \n}" % (self.name,
                                            ' '.join(map(lambda x: str(x), self.params)),
                                            '\n'.join(map(lambda x: str(x), self.body)))


def setParamOnModel(propName):
    return "set_property value [get_property value ${PARAM_VALUE.%s}] ${MODELPARAM_VALUE.%s}" % (propName, propName)

def paramManipulatorFns(paramName):
    pv = 'PARAM_VALUE.' + paramName
    yield TclFn("update_PARAM_VALUE." + paramName, [pv], [])
    yield TclFn("validate_PARAM_VALUE." + paramName, [pv], ["return true"])
    yield TclFn("update_MODELPARAM_VALUE." + paramName,
                ["MODELPARAM_VALUE." + paramName, pv],
                [setParamOnModel(paramName)])

# def makeDummyXGUIFile(fileName):
#    s = """
#    # Definitional proc to organize widgets for parameters.
# proc init_gui { IPINST } {
#  #Adding Page
#  ipgui::add_page $IPINST -name "Page 0"
#
# }"""
#    with open(fileName, "w") as f:
#        f.write(s)
