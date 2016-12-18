from jinja2.loaders import PackageLoader
from jinja2.environment import Environment

vhdlTmplEnv = Environment(loader=PackageLoader('hdl_toolkit', 'serializer/vhdl/templates'))

class VhdlVersion():
    v2002 = 2002
    v2008 = 2008