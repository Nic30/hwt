

def removeUnconnectedSignals(netlist):
    
    toDelete = set()
    for sig in netlist.signals:
        if not sig.endpoints:
            toDelete.add(sig)
            
    for sig in toDelete:
        netlist.signals.remove(sig)
    