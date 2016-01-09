#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re

from vhdl_toolkit.templates import VHDLTemplates as templ
from vhdl_toolkit.testbench_generator import TestbenchCreator, HWProcess
from vhdl_toolkit.types import VHDLType
from vhdl_toolkit.variables import SignalItem


#class HandShake_interface():
#    def __init__(self, rd, vld, sensitivityList):
#        self.vld = vld
#        self.rd = rd
#        # self.sensitivityList = sensitivityList
#        
#    def _onBouthHigh(self, rd, vld,):
#        # self.sensitivityList.add(vld)
#        return """{0} <= '1';
#        if {1} /= '1' then 
#            wait until {1} = '1';
#        end if;
#        """.format(rd, vld)
#    def _stop(self, rd):
#        return """
#        wait for clk_period;
#        {0} <= '0';
#        """.format(rd)
#    def _renderAssigments(self, assigmensts):
#        if assigmensts is not None or assigmensts == []:
#            return "\n".join([str(assignFrom) for assignFrom in assigmensts]) + "\n"
#        else:
#            return ""
#    def writeAccept(self, assigmensts=None):
#        return self._renderAssigments(assigmensts) + self._onBouthHigh(self.rd, self.vld) + self._stop(self.rd)
#    
#    def write(self, assigmensts=None):
#        return self._onBouthHigh(self.vld, self.rd) + self._renderAssigments(assigmensts) + self._stop(self.vld)
#
class HandShake_interface():
    def __init__(self, rd, vld, sensitivityList):
        self.vld = vld
        self.rd = rd
        # self.sensitivityList = sensitivityList
        
    def _onBouthHigh(self, rd, vld,):
        # self.sensitivityList.add(vld)
        return """{0} <= '1';
        if {1} /= '1' then 
            wait until {1} = '1';
        end if;
        """.format(rd, vld)
    def _stop(self, rd):
        return """
        wait for clk_period;
        {0} <= '0';
        """.format(rd)
    def _renderAssigments(self, assigmensts):
        if assigmensts is not None or assigmensts == []:
            return "\n".join([str(assignFrom) for assignFrom in assigmensts]) + "\n"
        else:
            return ""
    def writeAccept(self, assigmensts=None):
        return self._renderAssigments(assigmensts) + self._onBouthHigh(self.rd, self.vld) + self._stop(self.rd)
    
    def write(self, assigmensts=None):
        return self._onBouthHigh(self.vld, self.rd) + self._renderAssigments(assigmensts) + self._stop(self.vld)


class Axi4_a():
    def __init__(self, prefix, process, rw='w'):
        self.hs = HandShake_interface(prefix + "A" + rw + "READY", prefix + "A" + rw + "VALID", process.sensitivityList)
        self.prefix = prefix
        self.hs
        self.process = process
        self.rw = rw
        process.register(self)
    def init(self):
        return self.hs.init()
    def writeAccept(self, expectedAddr, expectedDataLen):
        return self.hs.writeAccept()

class Axi4_d():
    def __init__(self, prefix, process, rw='w'):
        self.prefix = prefix
        self.process = process
        self.rw = rw
        self.hs = HandShake_interface(prefix + rw + "READY", prefix + rw + "VALID", process.sensitivityList)
        process.register(self)
        
    def read(self, expectedData):
        buff = []
        for d in expectedData:
            buff.append("-- expected data %s" % (str(d)))
            buff.append(self.hs.writeAccept())
        return "\n".join(buff)
    
    def write(self, data, burstId):
        buff = []
        data_t = VHDLType()
        data_t.str = "std_logic_vector()"
        bit_t = VHDLType()
        bit_t.str = "std_logic"
        last = data[-1]
        for d in data:
            buff.append(self.hs.write([
                                       SignalItem(self.prefix + self.rw + "DATA", data_t).eq(d),
                                       SignalItem(self.prefix + self.rw + "ID", data_t).eq(burstId),
                                       SignalItem(self.prefix + self.rw + "LAST", bit_t).eq(last is d)
                                       ]))
        return "\n".join(buff)
            
class Axi4_b():
    resp_ok = 0
    def __init__(self, prefix, process):
        self.hs = HandShake_interface(prefix + "BREADY", prefix + "BVALID", process.sensitivityList)
        self.prefix = prefix
        self.process = process
        process.register(self)
        
    def write(self, resp):
        data_t = VHDLType()
        data_t.str = "std_logic_vector()"
        return self.hs.write([SignalItem(self.prefix + "BRESP", data_t).eq(resp)])
    def writeAccept(self):
        return self.hs.writeAccept()
        
class AXI4_slave(object):
    def __init__(self, prefix):
        self.prefix = prefix

        self.awProcess = HWProcess(prefix + "AW")
        self.aw = Axi4_a(prefix, self.awProcess, rw="w")
        self.arProcess = HWProcess(prefix + "AR")
        self.ar = Axi4_a(prefix, self.arProcess, rw="r")
        self.rProcess = HWProcess(prefix + "R")
        self.r = Axi4_d(prefix, self.rProcess, rw='r')
        self.wProcess = HWProcess(prefix + "W")
        self.w = Axi4_d(prefix, self.wProcess, rw='w')
        self.bProcess = HWProcess(prefix + "B")
        self.b = Axi4_b(prefix, self.bProcess)
        self.processes = [self.awProcess, self.arProcess, self.rProcess, self.wProcess, self.bProcess]
                
    def initInterface(self):
        return ""
    
    def readResp(self, expectedAddr, data, burstId=0):
        """ Accept read request and respond with data (iterable)"""
        self.ar.writeAccept(expectedAddr, len(data))
        self.r.write(data, burstId)
    def writeAccept(self, expectedAddr, data):
        """Accept write request and check if data matches (data must be iterable)"""
        self.aw.writeAccept(expectedAddr, len(data))
        self.w.read(data)
        self.b.write(Axi4_b.resp_ok)
    
    # def readResp(self, data, withLast=True):
    #    """ Accept read request and respond with data (iterable)"""
    #    return templ.AXI4_slave_read_resp.render(axi_prefix=self.prefix, data=data, withLast=withLast)
    #
    # def writeAccept(self, data, withLast=True):
    #    """Accept write request and check if data matches (data must be iterable)"""
    #    return templ.AXI4_slave_write_accept.render(axi_prefix=self.prefix, data=data, withLast=withLast)

class AXI_lite_master(object):    
    def __init__(self, prefix):
        self.prefix = prefix
        
    def initInterface(self):
        return ""
    
    def read(self, addr):
        return templ.axi_lite_read.render(axi_prefix=self.prefix, addr=int(addr))
    
    def write(self, addr, data):
        return templ.axi_lite_write.render(axi_prefix=self.prefix, addr=int(addr), data=data)

# class AXI4_master(AXI_lite_master):
#    def __init__(self, prefix):
#        super().__init__(prefix)
#
#    def initInterface(self):
#        return templ.axi4_init.render(axi_prefix=self.prefix)    

class AXI_testbench(TestbenchCreator):
    def __init__(self, entity):
        super().__init__(entity)
        self.interface = {}
        self.addClkProcess()
        self.addStimProcess(initialResetDelay=5)
    # def getSignalByName(self, name):
    #    for s in TestbenchCreator.get_signals(self.entity.port):
    #        if s.name == name:
    #            return s

   
def listAxiIterfaces(entity):
    for p in entity.port:
        m = re.match("(.*)_awaddr$", p.name)
        if m:
            yield m.group(1)
    
