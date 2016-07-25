from hls_toolkit.streamLvl.intfValueCont import IntfValueCont


def valObj(intf, exclude=set()):
    """
    Generate default value object for interface
    """
    if intf._interfaces:
        v = IntfValueCont(intf)
        for i in intf._interfaces:
            if i not in exclude:
                setattr(v, i._name, valObj(i, exclude))
                v._interfaces.append(i)
        return v
    else:
        return 0  # (default value)