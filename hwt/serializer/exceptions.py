
class SerializerException(Exception):
    pass


class UnsupportedEventOpErr(SerializerException):
    """
    Target HDL can not use event operator in this context, it usually
    has to be replaced by correct expression of sensitivity list
    """
