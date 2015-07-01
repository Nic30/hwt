

def applyReplacesOnFile(fileName, replaces, write=True):
    with open(fileName) as f:
        content = f.read()
    
    for r in replaces:
        content = content.replace(r, replaces[r])    
    if write:    
        with open(fileName, "w") as f:
            f.write(content)
    else:
        return content
    
def axi_m_integer_fix(wraperFName):
    #filename = "/home/nic30/Documents/vivado/axi4_tester_simple/axi4_tester_simple.srcs/sources_1/bd/top/ip/top_axi4_trans_tester_0_0/sim/top_axi4_trans_tester_0_0.vhd"
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