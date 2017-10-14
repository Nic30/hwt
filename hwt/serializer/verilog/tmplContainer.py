from jinja2.environment import Environment
from jinja2.loaders import PackageLoader


class VerilogTmplContainer():
    tmplEnv = Environment(loader=PackageLoader(
        'hwt', 'serializer/verilog/templates'))

    moduleHeadTmpl = tmplEnv.get_template('module_head.v')
    moduleBodyTmpl = tmplEnv.get_template('module_body.v')
    processTmpl = tmplEnv.get_template('process.v')
    ifTmpl = tmplEnv.get_template("if.v")
    componentInstanceTmpl = tmplEnv.get_template("component_instance.v")
    switchTmpl = tmplEnv.get_template("switch.v")
