
from python_toolkit.fileHelpers import applyReplacesOnFile
import re

def ipFix_2015_2(componentString):
    s = re.sub(r'spirit:order="[^"]*"', r"", componentString , flags=re.MULTILINE)
    return s
    
def axi_m_integer_fix(wraperFName):
    # filename = "/home/nic30/Documents/vivado/axi4_tester_simple/axi4_tester_simple.srcs/sources_1/bd/top/ip/top_axi4_trans_tester_0_0/sim/top_axi4_trans_tester_0_0.vhd"
    replaces = {
               "USER_VALUE : STD_LOGIC_VECTOR" : "USER_VALUE : INTEGER",
               "PROT_VALUE : STD_LOGIC_VECTOR" : "PROT_VALUE : INTEGER",
               "CACHE_VALUE : STD_LOGIC_VECTOR": "CACHE_VALUE : INTEGER",
               "TARGET_ADDR : STD_LOGIC_VECTOR": "TARGET_ADDR : INTEGER",
               'X"00000000"': "0",
               'B"000"':"0",
               'B"0011"':"3"      
               }
    applyReplacesOnFile(wraperFName, replaces)
   

def fix_wraper_to_downto(wraperFName):
    replaces = {
                "0 to 0" : "0 downto 0"
               }
    applyReplacesOnFile(wraperFName, replaces)
    
    
if __name__ == "__main__":
    fn = "/opt/Xilinx/Vivado/2015.2/data/ip/xilinx/blk_mem_gen_v8_2/component.xml"
    with open(fn) as f:
        s = ipFix_2015_2(f.read())
    with open(fn, "w") as f:
        f.write(s)    
    
    #s = """  <spirit:value spirit:resolve="user" spirit:id="PARAM_VALUE.Error_Injection_Type" spirit:choiceRef="choices_6" spirit:order="14">Single_Bit_Error_Injection</spirit:value>"""
        
    #s = '''<spirit:value spirit:resolve="user" spirit:id="PARAM_VALUE.AXI_Type" spirit:choiceRef="choices_1" spirit:order="4">AXI4_Full</spirit:value>
    #<spirit:value spirit:resolve="user" spirit:id="PARAM_VALUE.AXI_Type" spirit:choiceRef="choices_1" spirit:order="4">AXI4_Full</spirit:value>'''
    #s = ipFix_2015_2(s)    
    print(s)
