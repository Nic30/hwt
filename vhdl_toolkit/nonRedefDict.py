class RedefinitionErr(Exception):
    pass

class NonRedefDict(dict):
    def __setitem__(self, key, val):
        if key in self:
            raise RedefinitionErr(key)
        dict.__setitem__(self, key, val)
