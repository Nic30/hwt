from hls_toolkit.vivadoHLS.unit import VivadoHLSUnit
from vhdl_toolkit.synthetisator.shortcuts import synthetizeCls


class ExactMatcher(VivadoHLSUnit):
    _top = "exactMatch"
    _project = "exactMatcherVivadoHls"
    
    
if __name__ == "__main__":
    print(synthetizeCls(ExactMatcher))
    print(ExactMatcher._entity)