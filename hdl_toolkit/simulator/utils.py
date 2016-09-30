
def valueHasChanged(valA, valB):
    return valA.val is not valB.val or valA.vldMask != valB.vldMask
