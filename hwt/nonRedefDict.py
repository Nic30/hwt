class RedefinitionErr(Exception):
    pass

class NonRedefDict(dict):
    def __setitem__(self, key, val):
        if key in self and val is not self[key]:
            raise RedefinitionErr(key)
        dict.__setitem__(self, key, val)
