

def changeKey(dic, oldKey, newKey):
    v = dic[oldKey]
    del dic[oldKey]
    dic[newKey] = v