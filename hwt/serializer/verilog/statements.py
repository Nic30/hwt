from hdlConvertorAst.hdlAst._bases import iHdlStatement
from hdlConvertorAst.hdlAst._expr import HdlAll
from hdlConvertorAst.hdlAst._statements import HdlStmProcess, HdlStmWait,\
    HdlStmBlock
from hdlConvertorAst.to.verilog.constants import SIGNAL_TYPE
from hwt.hdl.assignment import Assignment
from hwt.hdl.block import HdlStatementBlock
from hwt.serializer.verilog.utils import verilogTypeOfSig


class ToHdlAstVerilog_statements():

    def as_hdl_Assignment(self, a: Assignment):
        blocking = False
        ver_sig_t = verilogTypeOfSig(a.dst)
        if ver_sig_t in (SIGNAL_TYPE.REG, SIGNAL_TYPE.PORT_REG):
            evDep = False
            for driver in a.dst.drivers:
                if driver._event_dependent_from_branch is not None:
                    evDep = True
                    break

            if not evDep or a.dst.virtual_only:
                blocking = True
        elif ver_sig_t in (SIGNAL_TYPE.WIRE, SIGNAL_TYPE.PORT_WIRE):
            blocking = True
        else:
            raise ValueError(ver_sig_t)

        a = super(ToHdlAstVerilog_statements, self).as_hdl_Assignment(a)
        a.is_blocking = blocking
        return a

    def can_pop_process_wrap(self, stms, hasToBeVhdlProcess):
        if hasToBeVhdlProcess:
            return False
        else:
            assert len(stms) == 1
            return True

    def has_to_be_process(self, proc: HdlStatementBlock):
        for o in proc._outputs:
            if verilogTypeOfSig(o) in (SIGNAL_TYPE.REG, SIGNAL_TYPE.PORT_REG):
                return True

        return False

    def as_hdl_HdlStatementBlock(self, proc: HdlStatementBlock) -> iHdlStatement:
        p = super(ToHdlAstVerilog_statements,
                  self).as_hdl_HdlStatementBlock(proc)
        if isinstance(p, HdlStmProcess):
            no_wait = True
            if isinstance(p.body, HdlStmWait):
                no_wait = False
            elif isinstance(p.body, HdlStmBlock):
                for _o in p.body.body:
                    if isinstance(_o, HdlStmWait):
                        no_wait = False
                        break
            if no_wait and not p.sensitivity:
                # all input are constant and that is why this process does not have
                # any sensitivity
                p.sensitivity = [HdlAll, ]

            # add label
            if not isinstance(p.body, HdlStmBlock):
                b = p.body
                p.body = HdlStmBlock()
                p.body.body.append(b)
            p.body.labels.extend(p.labels)
            p.labels.clear()
        return p
