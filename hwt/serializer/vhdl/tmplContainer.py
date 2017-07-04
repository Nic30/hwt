
from jinja2.environment import Environment
from jinja2.loaders import PackageLoader


class VhdlTmplContainer():
    tmplEnv = Environment(loader=PackageLoader('hwt', 'serializer/vhdl/templates'))
    architectureTmpl = tmplEnv.get_template('architecture.vhd')
    entityTmpl = tmplEnv.get_template('entity.vhd')
    processTmpl = tmplEnv.get_template('process.vhd')
    componentTmpl = tmplEnv.get_template('component.vhd')
    componentInstanceTmpl = tmplEnv.get_template('component_instance.vhd')
    ifTmpl = tmplEnv.get_template('if.vhd')
    switchTmpl = tmplEnv.get_template('switch.vhd')
