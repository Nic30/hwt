from hdl_toolkit.simulator.simModel import SimModel, sensitivity
from hdl_toolkit.synthesizer.rtlLevel.netlist import RtlNetlist
from hdl_toolkit.hdlObjects.assignment import mkUpdater, mkArrayUpdater
from hdl_toolkit.hdlObjects.types.defs import BIT, INT
from hdl_toolkit.hdlObjects.typeShortcuts import vecT
from hdl_toolkit.hdlObjects.types.enum import Enum
from hdl_toolkit.hdlObjects.types.array import Array
from hdl_toolkit.synthesizer.rtlLevel.rtlSignal import RtlSignal{% for c in componentInstances %}
from {{c.__class__.__name__}} import import {{c.__class__.__name__}}{% endfor %}
{% for imp in imports %}
{{imp}}
{% endfor %}

class {{ name }}(SimModel):
    _name = "{{ name }}" 
    _cntx = RtlNetlist()
    # ports{% for name, dtype in ports %}
    {{name}} = RtlSignal(_cntx, "{{name}}", {{dtype}}){% endfor %}
    
    # internal signals{% for name, dtype, defVal in signals %}
    {{name}} = RtlSignal(_cntx, "{{name}}", {{dtype}}, defVal={{defVal}}){% endfor %}
    
    {% for c in componentInstances %}
    {{c._name}} = {{c.__class__.__name__}}()
    {% endfor %}
{% for proc in processes %}
{{proc}}
{% endfor %}
    
    
    def __init__(self):
        self._interfaces = [{% for name, _ in ports   %}self.{{name}},
                            {% endfor %}{% for name, _, _ in signals %}self.{{name}},
                            {% endfor %}]
        self._processes = [{% for procName in processesNames %}self.{{procName}},
                           {% endfor %}]
        self._units = [{% for c in componentInstances %}self.{{c._name}},
                       {% endfor %}
                       ]
    
        
        