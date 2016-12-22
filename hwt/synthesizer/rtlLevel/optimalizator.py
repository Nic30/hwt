

def removeUnconnectedSignals(netlist):
    
    toDelete = set()
    while True:
        for sig in netlist.signals:
            if not sig.endpoints:
                try:
                    if sig._interface is not None:
                        continue
                except AttributeError:
                    pass
                toDelete.add(sig)
                
        if toDelete:        
            for sig in toDelete:
                netlist.signals.remove(sig)
            toDelete = set()
        else:
            return