

def removeUnconnectedSignals(netlist):
    
    toDelete = set()
    for sig in netlist.signals:
        if not sig.endpoints:
            try:
                if sig._interface is not None:
                    continue
            except AttributeError:
                pass
            toDelete.add(sig)
            
            
    for sig in toDelete:
        #print("rm", sig)
        netlist.signals.remove(sig)
    