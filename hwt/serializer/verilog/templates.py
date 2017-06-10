from jinja2.loaders import PackageLoader
from jinja2.environment import Environment

verilogTmplEnv = Environment(loader=PackageLoader('hwt', 'serializer/verilog/templates'))

moduleHeadTmpl = verilogTmplEnv.get_template('module_head.v')
moduleBodyTmpl = verilogTmplEnv.get_template('module_body.v')
processTmpl = verilogTmplEnv.get_template('process.v')
ifTmpl = verilogTmplEnv.get_template("if.v")
componentInstanceTmpl = verilogTmplEnv.get_template("component_instance.v")
