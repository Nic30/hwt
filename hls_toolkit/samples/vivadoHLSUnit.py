from hdl_toolkit.synthesizer.shortcuts import toRtl
from hls_toolkit.vivadoHLS.unit import VivadoHLSUnit


class ExactMatcher(VivadoHLSUnit):
    _top = "exactMatch"
    _project = "exactMatcherVivadoHls"
    
    
if __name__ == "__main__":
    print(toRtl(ExactMatcher))
    print(ExactMatcher._entity)