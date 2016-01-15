
import re
# '\s+in\s+\[\s*([^,\]]+)(\s*,\s*([^,\]]+))*\]'
inWithSingleElm = re.compile('\s+in\s+\[\s*([^,\]]+)\]')

with open('vhdlParser.py') as f:
    s = inWithSingleElm.sub(' == \g<1>', f.read())
    print(s)
    with open("vhdlParser.out.py", 'w') as fOut:
        fOut.write(s)