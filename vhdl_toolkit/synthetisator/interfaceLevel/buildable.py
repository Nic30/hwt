
class Buildable():
    """
        @cvar _clsIsBuild: if class has this attribute and it is True it means class was builded 
    """
    @classmethod
    def _isBuild(cls):
        return hasattr(cls, "_clsIsBuild")
    @classmethod
    def _builded(cls):
        if not hasattr(cls, "_clsIsBuild"):
            cls._build()   