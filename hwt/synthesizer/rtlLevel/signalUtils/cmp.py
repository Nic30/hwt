
def areSameSignals(a, b):
    if a is b:
        return True
    if type(a) != type(b):
        return False 
    if len(a.drivers) != 1 or len(b.drivers) != 1:
        return False
    da = list(a.drivers)[0]
    db = list(b.drivers)[0]
    return da == db