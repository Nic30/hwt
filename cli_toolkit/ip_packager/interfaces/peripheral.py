from cli_toolkit.ip_packager.interfaces.intfConfig import IntfConfig 


class IP_IIC(IntfConfig):
    def __init__(self):
        super().__init__()
        self.name = "iic"
        self.version = "1.0"
        self.vendor = "xilinx.com" 
        self.library = "interface"
        self.map = {'slc':{"t":"SLC_T",
                           "i": "SLC_I",
                           "o": "SLC_O"},
                    'sda':{"t": "SDA_T",
                           "i": "SDA_I",
                           "o": "SDA_O"}
                     }

class IP_Uart(IntfConfig):
    def __init__(self):
        super().__init__()
        self.name = "iic"
        self.version = "1.0"
        self.vendor = "xilinx.com" 
        self.library = "interface"
        self.map = {'rx':"RxD",
                    'tx':"TxD"}