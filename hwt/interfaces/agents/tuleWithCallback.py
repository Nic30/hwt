
class TupleWithCallback(tuple):

    def __new__(cls, *args, onDone=None):
        t = tuple.__new__(cls, args)
        if onDone is not None:
            t.onDone = onDone
        return t

