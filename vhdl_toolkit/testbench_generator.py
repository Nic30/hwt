#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from vhdl_toolkit.variables import SignalItem
from vhdl_toolkit.process import HWProcess
from vhdl_toolkit.parser import entityFromFile
from vhdl_toolkit.formater import formatVhdl
from vhdl_toolkit.templates import VHDLTemplates
 
class fifo():
    def __init__(self, name):
        self.name = name
    def write(self, data):
        return self.name + "_empty_n <= '1';" + self.name + "_rd_data<= std_logic_vector(to_unsigned(" + str(data) + ", " + self.name + "_rd_data'length));"
    def write_stop(self):
        return self.name + "_empty_n <= '0';" + self.name + "_rd_data<= std_logic_vector(to_unsigned(0, " + self.name + "_rd_data'length));"
    
    def read(self):
        return self.name + "_full_n <= '1';"
    def read_stop(self):  
        return self.name + "_full_n <= '0';"

def waitForHigh(sigName):
    buff = []
    buff.append("while (%s /= '1') loop" % sigName)
    buff.append(delay(1))
    buff.append("wait on %s;" % sigName)
    buff.append("end loop;")
    return buff
        
class hs():
    def __init__(self, name, clk_period_name):
        self.name = name
        self.vld = "_ap_vld"
        self.ack = "_ap_ack"
        self.data = ""
        self.clk_period_name = clk_period_name
        
    def write(self, data):
        buff = []
        buff.append(self.name + self.vld + " <= '1';")  
        buff.append(self.name + self.data + "<= std_logic_vector(to_unsigned(" + str(data) + ", " + self.name + self.data + "'length));")
        buff.extend(waitForHigh(self.name + self.ack))
        buff.append("wait for %s;" % self.clk_period_name)
        buff.append(self.name + self.vld + " <= '0';") 
        buff.append(self.name + self.data + "<= (others => 'X');")
        return buff 
   
    def write_stop(self):
        return self.name + self.vld + "<= '0';" + self.name + self.data + "<= std_logic_vector(to_unsigned(0, " + self.name + self.data + "'length));"
    
    def read(self):
        buff = []
        vld = self.name + self.vld
        buff.append(self.name + self.ack + "<= '1';")
        buff.extend(waitForHigh(vld))
        buff.append("wait for %s;" % self.clk_period_name)
        buff.append(self.name + self.ack + "<= '0';")
        return buff
    
    def read_stop(self):  
        return self.name + self.ack + "<= '0';"
    

class AxiStream(hs):
    def __init__(self, name, clk_period_name):
        super().__init__(name, clk_period_name)
        self.vld = "_TVALID"
        self.ack = "_TREADY"
        self.last = "_TLAST"
        self.data = "_TDATA"
    def readBurst(self, expectedData):
        buff = []
        for d in expectedData:
            buff.append(self.read())  # todo expected data   
        
        return buff
        
        
    def writeBurst(self, data):
        l = len(data)
        return [self.write(d, idx + 1 == l) for idx, d in enumerate(data)]
            
    def write(self, data, last):
        buff = []
        buff.append(self.name + self.last + " <= '" + str(int(last)) + "';")
        buff.extend(super().write(data))
        buff.append(self.name + self.last + " <= '0';")
        return  buff
    
    def write_stop(self):
        return super().write_stop() + "\n" + self.name + self.last + " <= '0';\n"

class axi_hs(hs):
    def __init__(self, name):
        super().__init__(self, name)
        self.vld = "_VALID"
        self.ack = "_READY"

def delay(clk):
    return "wait for clk_period *%d;" % (clk) 
 
def vhdlAssert(cond, msg, level):
    return 'assert %s report "%s" severity %s;' % (cond, msg, level)

def vhdlWarning(cond, msg):
    return vhdlAssert(cond, msg , "warning")

def vhdlErr(cond, msg):
    return vhdlAssert(cond, msg , "error")

def asUnsigned(sigName):
    return  "to_integer(unsigned(%s))" % sigName

 
class TestbenchCreator(object):
    def __init__(self, entity):
        self.entity = entity
        self.clkName = "ap_clk"
        self.resetName = self.findResetName(entity.port)
        if self.resetName.endswith("_n"):
            self.resetActiveIn = 0
        else:
            self.resetActiveIn = 1
        self.processes = []
    def findResetName(self, port):
        for p in port:
            if p.direction == p.typeIn and p.name.startswith("ap_rst"):
                return p.name 
    @staticmethod
    def get_signals(port):
        for p in port:
            s = str(SignalItem(p.name, p.var_type))
            if p.direction == 'IN':
                if p.var_type.str.lower() == "std_logic":
                    s += ":='0'"
                else:
                    if "strb" in p.name.lower():
                        s += ":=(others => '1')"
                    else:
                        s += ":=(others => '0')"
            yield s
            
    def register(self, interface):
        if hasattr(interface, "processes"):
            self.processes.extend(interface.processes)
        else:
            proc = HWProcess(interface.prefix + "_proc")
            proc.register(interface)
            self.processes.append(proc)
    
    def addStimProcess(self, initialResetDelay=10):
        stimP = HWProcess("stim_process")
        stimP.bodyBuff.append("""
        {0} <='{1}';        
        wait for clk_period *{2!s};
        {0} <='{3!s}'; 
        """.format(self.resetName, self.resetActiveIn, initialResetDelay, int(not int(self.resetActiveIn))))      
        self.processes.append(stimP)
        return stimP


    def addClkProcess(self):
        clkPeriod = "clk_period"
        clkP = HWProcess("clk_process")
        clkP.bodyBuff.append(
         """
         %s <= '0';
         wait for %s/2;
         %s <= '1';
         wait for %s/2;
         """ % (self.clkName, clkPeriod, self.clkName, clkPeriod))
        self.processes.append(clkP)

    def constructBody(self):
        for p in self.processes:
            if p.name == "clk_process":
                pass
            elif p.name == "stim_process":
                p.bodyBuff.append("wait;")
            else:
                p.bodyBuff.insert(0, "wait for clk_period *6;")
                p.bodyBuff.append("wait;")
        self.body = "\n".join([str(p) for p in self.processes])
            
    def render(self):
        self.constructBody()
        opts = {'entity_name' : self.entity.name,
            'entity_port' : ";\n".join([ str(p) for p in self.entity.port]),
            'entity_signals' : ";\n".join([ x for x in TestbenchCreator.get_signals(self.entity.port)]) + ";\n",
            'entity_port_map' : ",\n".join([ p.name + "=>" + p.name  for p in self.entity.port]),
            'body' : self.body,
            'reset_active_in' : str(self.resetActiveIn),
            'reset_deactive_in' : str(int(not int(self.resetActiveIn))),
            'clk_name' : self.clkName,
            'reset_name' :self.resetName 
            }
        return VHDLTemplates.tb.render(opts)

def tb_fromEntFile(fileName):
    entity = entityFromFile(fileName)
    tb = TestbenchCreator(entity)
    return tb

def vecAsig(name, val):
    return "%s <= std_logic_vector(to_unsigned(%d, %s'length));" % (name, val, name)
            
# if __name__ == "__main__":
#    # fileName = "/home/nic30/Documents/vivado/axi4_tester_simple/axi4_tester_simple.srcs/sources_1/imports/hdl/top_wrapper.vhd"
#    fileName = "/home/nic30/Documents/vivado/multififo_test/multififo_test.srcs/sources_1/bd/top/hdl/top_wrapper.vhd"
#    # fileName = sys.argv[1]
#
#    def write(ch, data):
#        s = "doWrite <= '1';\n" + \
#        vecAsig("writeCh_V", ch) + "\n" + \
#        vecAsig("write_in", data) + "\n" + \
#        """wait for clk_period;
#        doWrite <= '0';"""
#        return s
#    def read(ch):
#        s = "doRead <= '1';\n" + \
#        vecAsig("readCh_V", ch) + "\n" + \
#        """wait for clk_period;
#        doRead <= '0';"""
#        return s
#    unit = entityFromFile(fileName)
#    tb = TestbenchCreator(unit)
#    tb.addClkProcess()
#    stimP = tb.addStimProcess(initialResetDelay=2)
#    stimP.bodyBuff += [write(0, 1)]
#    stimP.bodyBuff += [write(0, 2)]
#    stimP.bodyBuff += [read(0)]
#    stimP.bodyBuff += [read(0)]
#    
#    stimP.bodyBuff += [write(3, 3)]
#    stimP.bodyBuff += [write(3, 4)]
#    stimP.bodyBuff += [read(3)]
#    stimP.bodyBuff += [read(3)]
#    
#    print(formatVhdl(tb.render()))
