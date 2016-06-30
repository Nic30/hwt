
def valHasChanged(sig):
    o = sig._oldVal
    n = sig._val
    return n.val != o.val \
         or n.eventMask != o.eventMask\
         or n.vldMask != o.vldMask
