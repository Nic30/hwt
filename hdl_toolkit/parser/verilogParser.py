from hdl_toolkit.parser.baseParser import BaseParser 
from hdl_toolkit.hdlObjects.reference import HdlRef

class VerilogParser(BaseParser):
    def typeFromJson(self, jType, ctx):
        try:
            t_name_str = jType['literal']['value']
        except KeyError:
            op = jType['binOperator']
            t_name = self.hdlRefFromJson(op['op0'])
            t = ctx.lookupLocal(t_name)
            specificator = self.exprFromJson(op['operands'][0], ctx)
            t = t.applySpecificator(specificator)
            t.forceVector = True
            return t
        t_name = HdlRef([t_name_str], self.caseSensitive)
        return ctx.lookupLocal(t_name)