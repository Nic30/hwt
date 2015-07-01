#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from vhdl_toolkit.architecture import SignalItem
from vhdl_toolkit.process import HWProcess
from vhdl_toolkit.parser import entityFromFile
from vhdl_toolkit.formater import get_indent
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
        
class hs():
    def __init__(self, name):
        self.name = name
        self.vld = "_ap_vld"
        self.ack = "_ap_ack"
    def write(self, data):
        return self.name + self.vld + " <= '1';\n" + self.name + "<= std_logic_vector(to_unsigned(" + str(data) + ", " + self.name + "'length));"
    def write_stop(self):
        return self.name + self.vld + "<= '0';" + self.name + "<= std_logic_vector(to_unsigned(0, " + self.name + "'length));"
    
    def read(self):
        return self.name + self.ack + "<= '1';"
    def read_stop(self):  
        return self.name + self.ack + "<= '0';"
    

class axi_hs(hs):
    def __init__(self, name):
        super().__init__(self, name)
        self.vld = "_VALID"
        self.ack = "_READY"

def delay(clk):
    return "wait for clk_period *%d;" % (clk) 
 
 
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
            'entity_port' : ";\n".join([get_indent(5) + str(p) for p in self.entity.port]),
            'entity_signals' : ";\n".join([ get_indent(5) + x for x in TestbenchCreator.get_signals(self.entity.port)]) + ";\n",
            'entity_port_map' : ",\n".join([get_indent(5) + p.name + "=>" + p.name  for p in self.entity.port]),
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
            
if __name__ == "__main__":
    fileName = "/home/nic30/Documents/vivado/axi4_tester_simple/axi4_tester_simple.srcs/sources_1/imports/hdl/top_wrapper.vhd"
    # fileName = sys.argv[1]
    entity = entityFromFile(fileName)
    tb = TestbenchCreator(entity)
    tb.addClkProcess()
    print(formatVhdl(tb.render()))