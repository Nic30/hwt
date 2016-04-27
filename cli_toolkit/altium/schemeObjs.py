from cli_toolkit.altium.schemeTypes import RecordTypes 

#https://github.com/vadmium/python-altium/blob/master/format.md

class Loscation():
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)

    def asDict(self):
        return {"LOCATION.X": str(self.x),
                "LOCATION.Y": str(self.y)}
 

class RecordCntx():
    def __init__(self):
        self.units = {}
    
#    def register(self, u):
#        if isinstance(u, SchComp):
#            u. 

class Record():
    def __init__(self):
        self.RECORD = None
        # other unclassified props
        self.p = {}
        
    @staticmethod
    def serializeObj(obj):
        if obj is None:
            return -1
        else:
            return obj.CURRENTPARTID

    @staticmethod
    def serializeIntVal(v):
        if v is None:
            return "-1"
        else:
            return str(v)
    
    @staticmethod
    def serializeBoolVal(v):
        if v:
            return "T"
        else:
            return "F"
        
    def setProp(self, propName, propVal):
        # existing = obj.get(name)
        # if existing not in (None, value):
        #    msg = "Conflicting duplicate: {!r}, was {!r}"
        #    warn(msg.format(property, existing))
        # obj[name] = value
        try:
            self.__dict__[propName]
            setattr(self, propName, propVal)
        except KeyError:
            self.p[propName] = propVal
    
    def asDict(self):
        d = {"RECORD" : self.RECORD}
        d.update(self.p)
        return d
        
    def __repr__(self):
        recTypeName = 'Unknown (%s)' % (str(self.RECORD)) 
        # resolve type name
        for k, v in RecordTypes.__dict__.items():
            if self.RECORD == v:
                recTypeName = k
        p = '|'.join(sorted(
                            map(lambda x: x[0] + '=' + str(x[1]),
                                self.p.items()
                                )
                            )
                     )
        return "<%s, RECORD:%s|%s>" % (self.__class__.__name__, recTypeName, p)

class SchSheet():
    def __init__(self, notClasifiedProps):
        self.p = notClasifiedProps
        self.childs = []
    
    def loadChilds(self, recordIterator):
        raise NotImplementedError()
    
    

class SchComp(Record):
    """
    @ivar designItemId: name of component in sheet 
    @ivar location: location object, describes absolute location of this component in sheet
    @ivar partCnt: integer: Number of separated parts within component 
          (e.g. there might be four parts in a quad op-amp component). 
          The value seems to be one more than you would expect, so 2 implies a normal
          component, and the quad op-amp would have 5.
    @ivar ownerPart: parent object
    @ivar displayModeCnt: integer: Number of alternative symbols for part
    """
    def __init__(self, UniqueId, name, location,
                 libReference,
                 sourceLibName,  # name of parent component in library
                 libPath='*',
                 targetFilename='*',
                 owner=None,
                 displayModeCnt=1,
                 notUsedBTableName=True,
                 areaColor=11599871,
                 color=128,
                 partCnt=1,
                 currentPartId=1,
                 partIdLocked=True):
        """
        not used:
        INDEXINSHEET
        """
        
        super(SchComp, self).__init__()
        self.RECORD = RecordTypes.SCH_COMPONENT
        
        self.designItemId = name  # b'universal DC/DC',
        self.partCnt = partCnt  # b'2',
        self.partIdLocked = partIdLocked  # b'T'
        self.currentPartId = currentPartId  # b'1' 
        self.uniqueId = UniqueId  # b'HGUGRXRR',

        # LOCATION.X b'390', LOCATION.Y b'390',
        self.location = location 

        # OWNERPARTID b'-1'
        assert(isinstance(owner, SchComp) or owner is None)
        self.ownerPart = ownerPart
        
        assert(isinstance(displayModeCnt, int))
        self.displayModeCnt = displayModeCnt  # b'1',
        
        assert(isinstance(notUsedBTableName, bool))
        self.notUsedBTableName = notUsedBTableName  # b'T',
        self.areaColor = areaColor  # b'11599871', 


        self.libRef = libReference  # b'universal DC/DC',
        self.sourceLibName = sourceLibName  # b'Altium_okruh_miscLib.IntLib'
        self.libPath = libPath  # ': b'*'
        self.targetFilename = targetFilename  # b'*',

        self.color = color  # b'128'
    
    #def deserialize(self, loadedObjs, selfDict):
    #    
        
        
    
    def asDict(self):
        
        d = super(SchComp, self).asDict()
        d.update(self.location.asDict())
        d["OWNERPARTID"] = str(Record.serializeObj(self.ownerPart))
        d['DISPLAYMODECOUNT'] = str(self.displayModeCnt)
        d['NOTUSEDBTABLENAME'] = Record.serializeBoolVal(self.notUsedBTableName) 
        d['AREACOLOR'] = str(self.areaColor)
        d['DESIGNITEMID'] = self.designItemId
        d['PARTCOUNT'] = Record.serIntVal(self.partCnt)
        d['PARTIDLOCKED'] = Record.serializeBoolVal(self.partIdLocked)
        d['CURRENTPARTID'] = Record.serIntVal(self.currentPartId)
        d['UNIQUEID'] = self.uniqueId
        d['LIBREFERENCE'] = self.libRef
        d['SOURCELIBRARYNAME'] = self.sourceLibName
        d['LIBRARYPATH'] = self.libPath
        d['TARGETFILENAME'] = self.targetFilename
        d['COLOR'] = str(self.color)
        
        return d
        
