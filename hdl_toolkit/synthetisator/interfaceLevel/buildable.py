class Buildable():
    """
        @cvar _clsIsBuild: if class has this attribute and it is True it means class was builded 
    """
    @classmethod
    def _isBuild(cls):
        return hasattr(cls, "_clsBuildFor") and cls._clsBuildFor == cls
    
    @classmethod
    def _builded(cls, multithread=True):
        if not cls._isBuild():
            cls._build(multithread=multithread)   
