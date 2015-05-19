#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import jinja2, re, os
from vhdl_toolkit.testbench_generator import TestbenchCreator, entityFromFile
from vhdl_toolkit.vhdl_simple_formater import formatVhdl
from vivado_toolkit.vivado_ip_wrap_fix import axi_m_integer_fix 
def fromTemplateFile(fileName, dataDict):
        with open(fileName) as f:
            template = jinja2.Template(f.read())
        return template.render(dataDict)
    
class AXI4_slave(object):
    def __init__(self, prefix):
        self.prefix = prefix
        
    def initInterface(self):
        return ""
    
    def readResp(self, data):
        return fromTemplateFile("templates_vhdl/AXI4_slave_read_resp.vhd",
                                {"axi_prefix": self.prefix,
                                 "data"      : data
                                 })
    def writeAccept(self):
        return fromTemplateFile("templates_vhdl/AXI4_slave_write_accept.vhd",
                                {"axi_prefix": self.prefix
                                 })

class AXI_lite_master(object):    
    def __init__(self, prefix):
        self.prefix = prefix
        
    def initInterface(self):
        return ""
    
    def read(self, addr):
        return fromTemplateFile("templates_vhdl/axi_lite_read.vhd",
                                 {"axi_prefix": self.prefix,
                                 "addr"      : addr
                                 })
    
    def write(self, addr, data):
        return fromTemplateFile("templates_vhdl/axi_lite_write.vhd",
                                 {"axi_prefix": self.prefix,
                                 "addr"      : addr,
                                 "data"      : data
                                 })

class AXI4_master(AXI_lite_master):
    def __init__(self, prefix):
        super().__init__(prefix)

    def initInterface(self):
        return fromTemplateFile("templates_vhdl/axi4_init.vhd",
                                 {"axi_prefix": self.prefix})    

class AXI_testbench(TestbenchCreator):
    overloadedMethods = ['write', 'read', 'readResp', 'writeAccept']
    def __init__(self, entity):
        super().__init__(entity)
        self.interface = {}
        self.body_buff = []
    def delay(self, clkCnt):
        self.body_buff.append("wait for clk_period * %d;" % (clkCnt))
    
    def logToStimProcWrap(self, func):
        def fnWithLogToStimProc(*args, **kwargs):
            cmdstr = func(*args, **kwargs)
            self.body_buff.append(cmdstr)
            return cmdstr
        return fnWithLogToStimProc
        
    def asignInterfaceClass(self, name, ifClass):
        self.interface[name] = ifClass(name)
        obj = self.interface[name]
        for attr in self.overloadedMethods:
            if hasattr(obj, attr):
                ovrld = self.logToStimProcWrap(getattr(obj, attr))
                setattr(obj, attr, ovrld)
        return obj

    def render(self):
        simProcessStr = "\n".join([ self.interface[x].initInterface() for x in self.interface ])
        self.process_stim = simProcessStr + "\n" + "\n".join(self.body_buff)
        return super().render()
    
def listAxiIterfaces(entity):
    for p in entity.port:
        m = re.match("(.*)_awaddr$", p.name)
        if m:
            yield m.group(1)

def axi4_tester():
    fileName = "/home/nic30/Documents/vivado/axi4_tester_simple/axi4_tester_simple.srcs/sources_1/bd/top/hdl/top_wrapper.vhd"
    #outputFile = "/home/nic30/Documents/vivado/axi4_tester_simple/axi4_tester_simple.srcs/sim_1/new/top_wraper_tb.vhd"
    entity = entityFromFile(fileName)
    # listAxiIterfaces(entity)
    tb = AXI_testbench(entity)
    axi4lite = tb.asignInterfaceClass('s_axi_AXILiteS_r_', AXI_lite_master)
    axi4 = tb.asignInterfaceClass('m_axi_data_', AXI4_slave)
    tb.delay(10)
    
    # CONTROLL_REG = 0x10
    # PACKET_SIZE_REG = 0x18
    # CNT_REG = 0x20
    
    CONTROLL_REG = 0x00
    CNT_REG = 0x10
    INIT_REG = 0x18
    PACKET_SIZE_REG = 0x20
    BASE_ADDR_REG = 0x28
    
    # axi4lite.read(CNT_REG)
    axi4lite.write(INIT_REG, 1)
    axi4lite.write(BASE_ADDR_REG, 128)
    axi4lite.write(PACKET_SIZE_REG, 1)
    axi4lite.write(CONTROLL_REG, 1);
    tb.delay(50)
    axi4lite.write(INIT_REG, 0)
    axi4lite.write(CONTROLL_REG, 1 + 128);
    # axi4lite.write(INIT_REG, 0)
    axi4.readResp(0xAAAA)
    axi4.writeAccept()

    axi4lite.read(CNT_REG)
    for _ in range(10):
        axi4.readResp(0xAAAA)
        axi4.writeAccept()
    
    axi4lite.read(CNT_REG)
if __name__ == "__main__":
    projectSrcPath = "/home/nic30/Documents/vivado/axi4_tester_coordinator_simple/axi4_tester_coordinator_simple.srcs/"
    fileName = os.path.join(projectSrcPath, "sources_1/bd/top/hdl/top_wrapper.vhd")
    outputFile = os.path.join(projectSrcPath, "sim_1/new/axi4_tester_coordinator_tb.vhd")
    entity = entityFromFile(fileName)
    # listAxiIterfaces(entity)
    tb = AXI_testbench(entity)
    axi4lite = tb.asignInterfaceClass('s_axi_AXILiteS_r_', AXI_lite_master)
    axi4 = tb.asignInterfaceClass('m_axi_gmem64_', AXI4_slave)
    tb.delay(10)
    CONTROLL_REG = 0x00
    TESTER_ADDR_REG = 0x10
    DELAY_REG = 0x18
    
    axi4lite.write(TESTER_ADDR_REG, 0x01)
    axi4lite.write(DELAY_REG, 30)
    axi4lite.write(CONTROLL_REG, 1)
    
    axi4.writeAccept()
    axi4.writeAccept()
    axi4.writeAccept()
    axi4.writeAccept()
    
        
    s = formatVhdl(tb.render())
    with open(outputFile, "w") as f:
        f.write(s)
    axi_m_integer_fix(os.path.join(projectSrcPath, "sources_1/bd/top/ip/top_axi4_trans_tester_coordinator_0_0/sim/top_axi4_trans_tester_coordinator_0_0.vhd"))
    print(s)
    
