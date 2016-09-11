

def sensitivity(*sensitiveTo):
    """
    register sensitivity for process
    and bound process int
    """
    def _sensitivity(proc):
        proc.sensitivityList = sensitiveTo 
        return proc
    
    return _sensitivity

class SimModel(object):
    pass
    