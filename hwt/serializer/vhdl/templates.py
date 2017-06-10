from jinja2.loaders import PackageLoader
from jinja2.environment import Environment

vhdlTmplEnv = Environment(loader=PackageLoader('hwt', 'serializer/vhdl/templates'))


IfTmpl = vhdlTmplEnv.get_template('if.vhd')
SwitchTmpl = vhdlTmplEnv.get_template('switch.vhd')
architectureTmpl = vhdlTmplEnv.get_template('architecture.vhd')
entityTmpl = vhdlTmplEnv.get_template('entity.vhd')
processTmpl = vhdlTmplEnv.get_template('process.vhd')
componentTmpl = vhdlTmplEnv.get_template('component.vhd')
componentInstanceTmpl = vhdlTmplEnv.get_template('component_instance.vhd')
