from hls_toolkit.vivadoHLS.unit import VivadoHLSUnit
from hdl_toolkit.synthetisator.shortcuts import toRtl


class ExactMatcher(VivadoHLSUnit):
    _top = "exactMatch"
    _project = "exactMatcherVivadoHls"
    
    
if __name__ == "__main__":
    print(toRtl(ExactMatcher))
    print(ExactMatcher._entity)