import struct
from io import SEEK_CUR
from warnings import warn

# may differs in python3
from PIL.OleFileIO import OleFileIO

from cli_toolkit.altium.schemeObjs import Record 

#http://www.eurointech.ru/products/Altium/Protel99SE_PCB_ASCII_File_Format.pdf

def readSchDoc(fileName):
    """Returns a iterator over all objects from an Altium *.SchDoc schematic file
    """
    ole = OleFileIO(fileName)
    # usualy contains: ['Additional', 'FileHeader','Storage']
    stream = ole.openstream("FileHeader")
    while True:
        length = stream.read(4)
        if not length:
            break
        (length,) = struct.unpack("<I", length)
        
        properties = stream.read(length - 1)
        obj = Record()
        for property in properties.split(b"|"):
            if not property:
                # Most (but not all) property lists are
                # prefixed with a pipe "|",
                # so ignore an empty property before the prefix
                continue
            
            (name, value) = property.split(b"=", 1)
            name = name.decode("utf-8")
            
            # try:
            #    value = value.decode("utf-8")
            # except UnicodeDecodeError:
            #    warn("value %s can not be converted to utf-8" % (str(value)))
            
            obj.setProp(name, value)

        
        yield  obj
        
        # Skip over null terminator byte
        stream.seek(+1, SEEK_CUR)
    


if __name__ == "__main__":
    for o in readSchDoc('samples/testSheet.SchDoc'):
        print(o)
