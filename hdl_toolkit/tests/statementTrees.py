import unittest
from hdl_toolkit.synthetisator.rtlLevel.context import Context
from hdl_toolkit.synthetisator.rtlLevel.signal.utils import connect
from hdl_toolkit.synthetisator.rtlLevel.codeOp import If, Switch
from hdl_toolkit.synthetisator.assigRenderer import renderIfTree
from hdl_toolkit.hdlObjects.statements import IfContainer, SwitchContainer
from hdl_toolkit.hdlObjects.types.defs import INT
from hdl_toolkit.hdlObjects.types.enum import Enum
import re
from hdl_toolkit.formater import formatVhdl


w = connect

rmWhitespaces = re.compile(r'\s+', re.MULTILINE)

class StatementTreesTC(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)
        self.c = Context("test")
    
    def compareStructure(self, template, cont):
        self.assertIsInstance(cont, template.__class__)
        if isinstance(template, IfContainer):
            self.assertEqual(template.cond, cont.cond)

            self.assertEqual(len(template.ifTrue), len(template.ifTrue))
            self.assertEqual(len(template.elIfs), len(template.elIfs))
            self.assertEqual(len(template.ifFalse), len(template.ifFalse))
        elif isinstance(template, SwitchContainer):
            self.assertEqual(template.switchOn, template.switchOn)
            self.assertEqual(len(template.cases), len(template.cases))
    
    def strStructureCmp(self, tmpl, cont):  
        cont = formatVhdl(str(cont))
        _tmpl = rmWhitespaces.sub(" ", tmpl).strip()
        _cont = rmWhitespaces.sub(" ", cont).strip()
    
        self.assertEquals(_tmpl, _cont, "%s\n\nshould be\n\n%s"% (cont, tmpl ))
    
    def test_baicIf(self):
        a = self.c.sig('a')
        b = self.c.sig('b')
        
        assigs = If(a,
           w(1, b)
           ,
           w(0, b)
        )
        
        container = list(renderIfTree(assigs))
        self.assertEqual(len(container), 1)
        container = container[0]
        tmpl = IfContainer([a], ifTrue=[w(1, b)], ifFalse=[w(0, b)])
        
        self.compareStructure(tmpl, container)
        
    def test_basicSwitch(self):
        a = self.c.sig('a', typ=INT)
        b = self.c.sig('b', typ=INT)
        
        assigs = Switch(a,
               *[(i, w(i, b)) for i in range(4)]
               )
        cont = list(renderIfTree(assigs))
        self.assertEqual(len(cont), 1)
        cont = cont[0]
        
        tmpl = SwitchContainer(a, [(i, w(i, b)) for i in range(3)] + [(None, w(3, b))])
        self.compareStructure(tmpl, cont)
    
    def test_ifsInSwitch(self):
        c = self.c
        stT = Enum('t_state', ["idle", "tsWait", "ts0Wait", "ts1Wait", "lenExtr"])
        clk = c.sig('clk')
        rst = c.sig("rst")
        
        st = c.sig('st', stT, clk=clk, syncRst=rst, defVal=stT.idle)
        sd0 = c.sig('sd0')
        sd1 = c.sig('sd1')
        cntrlFifoVld = c.sig('ctrlFifoVld')
        cntrlFifoLast = c.sig('ctrlFifoLast')
    
        def tsWaitLogic():
            return If(sd0 & sd1,
                       w(stT.lenExtr, st)
                       ,
                       w(stT.ts1Wait, st)
                    )
        assigs = Switch(st,
            (stT.idle,
                tsWaitLogic()
            ),
            (stT.tsWait,
                tsWaitLogic()
            ),
            (stT.ts0Wait,
                If(sd0,
                   w(stT.lenExtr, st)
                   ,
                   w(st, st)
                )
            ),
            (stT.ts1Wait,
                If(sd1,
                   w(stT.lenExtr, st)
                   ,
                   w(st, st)
                )
            ),
            (stT.lenExtr,
                If(cntrlFifoVld & cntrlFifoLast,
                   w(stT.idle, st)
                   ,
                   w(st, st)
                )
            )
        )
    
        cont = list(renderIfTree(assigs))
        self.assertEqual(len(cont), 1)
        cont = cont[0]
        tmpl ="""
        CASE st IS
            WHEN idle =>
                IF (sd0 AND sd1)='1' THEN 
                    st_next <= lenExtr;
                ELSE 
                    st_next <= ts1Wait;
                END IF;
            WHEN tsWait =>
                IF (sd0 AND sd1)='1' THEN 
                    st_next <= lenExtr;
                ELSE 
                    st_next <= ts1Wait;
                END IF;
            WHEN ts0Wait =>
                IF (sd0)='1' THEN 
                    st_next <= lenExtr;
                ELSE 
                    st_next <= st;
                END IF;
            WHEN ts1Wait =>
                IF (sd1)='1' THEN 
                    st_next <= lenExtr;
                ELSE 
                    st_next <= st;
                END IF;
            WHEN OTHERS =>
                IF (ctrlFifoVld AND ctrlFifoLast)='1' THEN 
                    st_next <= idle;
                ELSE 
                    st_next <= st;
                END IF;
        END CASE
        
        """
        self.strStructureCmp(tmpl, cont)
    
    def test_ifs2LvlInSwitch(self):
        c = self.c
        stT = Enum('t_state', ["idle", "tsWait", "ts0Wait", "ts1Wait", "lenExtr"])
        clk = c.sig('clk')
        rst = c.sig("rst")
        
        st = c.sig('st', stT, clk=clk, syncRst=rst, defVal=stT.idle)
        sd0 = c.sig('sd0')
        sd1 = c.sig('sd1')
        cntrlFifoVld = c.sig('ctrlFifoVld')
        cntrlFifoLast = c.sig('ctrlFifoLast')
    
        def tsWaitLogic(ifNoTsRd):
            return If(sd0 & sd1,
                       w(stT.lenExtr, st)
                       ,
                       ifNoTsRd
                    )
        assigs = Switch(st,
            (stT.idle,
                tsWaitLogic(
                    If(cntrlFifoVld,
                       w(stT.tsWait, st)
                       ,
                       w(st, st)
                    )
                )
            ),
            (stT.tsWait,
                tsWaitLogic(w(st, st))
            ),
            (stT.ts0Wait,
                If(sd0,
                   w(stT.lenExtr, st)
                   ,
                   w(st, st)
                )
            ),
            (stT.ts1Wait,
                If(sd1,
                   w(stT.lenExtr, st)
                   ,
                   w(st, st)
                )
            ),
            (stT.lenExtr,
                If(cntrlFifoVld & cntrlFifoLast,
                   w(stT.idle, st)
                   ,
                   w(st, st)
                )
            )
        )
    
        cont = list(renderIfTree(assigs))
        self.assertEqual(len(cont), 1)
        cont = cont[0]
        tmpl ="""
        CASE st IS
            WHEN idle =>
                IF (sd0 AND sd1)='1' THEN 
                    st_next <= lenExtr;
                ELSIF (ctrlFifoVld)='1' THEN 
                    st_next <= tsWait;
                ELSE 
                    st_next <= st;
                END IF;
            WHEN tsWait =>
                IF (sd0 AND sd1)='1' THEN 
                    st_next <= lenExtr;
                ELSE 
                    st_next <= st;
                END IF;
            WHEN ts0Wait =>
                IF (sd0)='1' THEN 
                    st_next <= lenExtr;
                ELSE 
                    st_next <= st;
                END IF;
            WHEN ts1Wait =>
                IF (sd1)='1' THEN 
                    st_next <= lenExtr;
                ELSE 
                    st_next <= st;
                END IF;
            WHEN OTHERS =>
                IF (ctrlFifoVld AND ctrlFifoLast)='1' THEN 
                    st_next <= idle;
                ELSE 
                    st_next <= st;
                END IF;
        END CASE
        
        """
        self.strStructureCmp(tmpl, cont)
    
    def test_ifs3LvlInSwitch(self):
        c = self.c
        stT = Enum('t_state', ["idle", "tsWait", "ts0Wait", "ts1Wait", "lenExtr"])
        clk = c.sig('clk')
        rst = c.sig("rst")
        
        st = c.sig('st', stT, clk=clk, syncRst=rst, defVal=stT.idle)
        sd0 = c.sig('sd0')
        sd1 = c.sig('sd1')
        cntrlFifoVld = c.sig('ctrlFifoVld')
        cntrlFifoLast = c.sig('ctrlFifoLast')
    
        def tsWaitLogic(ifNoTsRd):
            return If(sd0 & sd1,
                       w(stT.lenExtr, st)
                       ,
                       If(sd0,
                          w(stT.ts1Wait, st)
                          ,
                          ifNoTsRd
                       )
                    )
        assigs = Switch(st,
            (stT.idle,
                tsWaitLogic(
                    If(cntrlFifoVld,
                       w(stT.tsWait, st)
                       ,
                       w(st, st)
                    )
                )
            ),
            (stT.tsWait,
                tsWaitLogic(w(st, st))
            ),
            (stT.ts0Wait,
                If(sd0,
                   w(stT.lenExtr, st)
                   ,
                   w(st, st)
                )
            ),
            (stT.ts1Wait,
                If(sd1,
                   w(stT.lenExtr, st)
                   ,
                   w(st, st)
                )
            ),
            (stT.lenExtr,
                If(cntrlFifoVld & cntrlFifoLast,
                   w(stT.idle, st)
                   ,
                   w(st, st)
                )
            )
        )
    
        cont = list(renderIfTree(assigs))
        self.assertEqual(len(cont), 1)
        cont = cont[0]
        tmpl ="""
        CASE st IS
            WHEN idle =>
                IF (sd0 AND sd1)='1' THEN 
                    st_next <= lenExtr;
                ELSIF (sd0)='1' THEN
                    st_next <= ts1Wait; 
                ELSIF (ctrlFifoVld)='1' THEN 
                    st_next <= tsWait;
                ELSE 
                    st_next <= st;
                END IF;
            WHEN tsWait =>
                IF (sd0 AND sd1)='1' THEN 
                    st_next <= lenExtr;
                ELSIF (sd0)='1' THEN
                    st_next <= ts1Wait;
                ELSE 
                    st_next <= st;
                END IF;
            WHEN ts0Wait =>
                IF (sd0)='1' THEN 
                    st_next <= lenExtr;
                ELSE 
                    st_next <= st;
                END IF;
            WHEN ts1Wait =>
                IF (sd1)='1' THEN 
                    st_next <= lenExtr;
                ELSE 
                    st_next <= st;
                END IF;
            WHEN OTHERS =>
                IF (ctrlFifoVld AND ctrlFifoLast)='1' THEN 
                    st_next <= idle;
                ELSE 
                    st_next <= st;
                END IF;
        END CASE
        
        """
        self.strStructureCmp(tmpl, cont)
if __name__ == '__main__':
    suite = unittest.TestSuite()
    #suite.addTest(StatementTreesTC('test_basicSwitch'))
    suite.addTest(unittest.makeSuite(StatementTreesTC))
    runner = unittest.TextTestRunner(verbosity=3)
    runner.run(suite)
