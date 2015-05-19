

import xml.etree.ElementTree as et
brdFile =  '/home/nic30/Documents/vivado/axi4_tester2/axi4_tester2.srcs/sources_1/bd/main.bd'
filename = "/home/nic30/Documents/vivado_hls/axi4_trans_tester/solution1/impl/ip/component.xml"

registersPath  = "./memoryMaps/register"
zynqPath = './component'


x = et.parse(filename)
root = x.getroot()
root.findall()
print(root)