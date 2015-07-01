from hls_toolkit.debug import translate_syntax_error

class HLSTeplateErr(BaseException):
    """ error in hls file """
    @classmethod
    def _raise(cls, msg, fileName, lineNo):
        try:
            raise cls(msg)
        except cls as e:
            e.filename = fileName
            e.lineno = lineNo
            translate_syntax_error(e)
            raise e
    
    @classmethod
    def _raiseFromFn(cls, msg, fn):
        cls._raise(msg, fn.__code__.co_filename, fn.__code__.co_firstlineno)

class ConfError(HLSTeplateErr):
    """Error in hls configuration"""
    pass

class MissingConfAttribErr(ConfError):
    """Missing error in hls configuration"""
    pass

class InvalidAsign(Exception):
    pass

class UnimplementedErr(Exception):
    pass