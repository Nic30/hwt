
class LangueKeyword(object):
    pass

class NameOccupiedErr(Exception):
    def __init__(self, usedOn):
        self.usedOn = usedOn

class NameScopeItem(dict):
    """
    if name is discovered in scope it is converted to name_id
    where id is sequential number for prefix name_
    """
    def __init__(self, myLvl):
        super().__init__()
        self.myLvl = myLvl

        # some names are specified just as prefix and serializer 
        # should resolve correct name for object
        # this happens for most of generated objects
        self.cntrsForPrefixNames = {}
    
    def getChild(self, parent):
        try:
            return parent[self.myLvl + 1]
        except IndexError:
            return None
        
    def getParent(self, parent):

        i = self.myLvl - 1
        if i < 0:
            return None
        else:
            return parent[self.myLvl - 1]

    def __incrPrefixCntrsForChilds(self, prefix, currentVal, parent):
        # [TODO] check if new name is not defined in any direction
        currentVal += 1
        self.cntrsForPrefixNames[prefix] = currentVal
        ch = self.getChild(parent)
        while ch:
            if prefix in ch.cntrsForPrefixNames:
                ch.cntrsForPrefixNames[prefix] = currentVal
                ch = ch.getChild(parent)
            else:
                # prefix is not registered at any child
                break
            
        usableName = prefix + str(currentVal)
        return usableName
    
    def __registerName(self, name, obj, parent):
        # search if name is already defined on me and parents
        actual = self
        o = None
        
        if parent.ignorecase:
            _name = name.lower()
        else:
            _name = name
            
        while actual is not None:
            try:
                o = actual[_name]
            except KeyError:
                actual = actual.getParent(parent)
                continue
            break
        
        if o is None or o is obj: 
            # we can use use the name, because it is not used
            self[_name] = obj
        else:
            raise NameOccupiedErr(o)
            
    def getUsableName(self, suggestedName, obj, parent):
        if not suggestedName.endswith("_"):
            try:
                self.__registerName(suggestedName, obj, parent)
                return suggestedName
            except NameOccupiedErr:
                suggestedName += "_"
        
        actual = self
        try:
            cntrVal = actual.cntrsForPrefixNames[suggestedName]
        except KeyError:
            cntrVal = -1
        
        # setup for me and propagate to children
        usableName = self.__incrPrefixCntrsForChilds(suggestedName, cntrVal, parent)
        self.__registerName(usableName, obj, parent)
        return usableName
    
class NameScope(list):
    """
    Scope of used names in hdl
    """
    def __init__(self, ignorecase):
        super().__init__()
        self.ignorecase = ignorecase 
    
    def fork(self, lvl):
        f = NameScope(self.ignorecase)
        for i in range(lvl):
            f.append(self[i])
        return f
        
    def setLevel(self, lvl):
        """
        Trim or extend scope
        lvl = 1 -> only one scope (global)
        """
        while len(self) != lvl:
            if len(self) > lvl:
                self.pop()
            else:
                self.append(NameScopeItem(len(self)))

    def checkedName(self, actualName, actualObj, isGlobal=False):
        if isGlobal:
            return self[0].getUsableName(actualName, actualObj, self)
        else:
            return self[-1].getUsableName(actualName, actualObj, self)
