from hdl_toolkit.simulator.simModel import SimModel, sensitivity
from hdl_toolkit.synthesizer.rtlLevel.netlist import RtlNetlist
from hdl_toolkit.hdlObjects.assignment import mkUpdater, mkArrayUpdater
from hdl_toolkit.hdlObjects.types.defs import BIT, INT
from hdl_toolkit.hdlObjects.typeShortcuts import vecT
from hdl_toolkit.hdlObjects.types.enum import Enum
from hdl_toolkit.hdlObjects.types.array import Array
from hdl_toolkit.synthesizer.rtlLevel.rtlSignal import RtlSignal{% for c in componentInstances %}
if "{{c.name}}" not in locals(): # support for all models in single file
    from {{c.name}} import {{c.name}}{% endfor %}
{% for imp in imports %}
{{imp}}
{% endfor %}

class {{ name }}(SimModel):
    _name = "{{ name }}" 
    _cntx = RtlNetlist()
    # ports{% for name, dtype in ports %}
    {{name}} = RtlSignal(_cntx, "{{name}}", {{dtype}}){% endfor %}
    
    # internal signals{% for name, dtype, defVal in signals %}
    {{name}} = RtlSignal(_cntx, "{{name}}", {{dtype}}, defaultVal={{defVal}}){% endfor %}
    
    {% for c in componentInstances %}
    {{c._name}} = {{c.name}}()
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
        {% for proc in processObjects %}
        sensitivity(self.{{proc.name}}, {% for s in proc.sensitivityList %}self.{{s.name}}, {% endfor %})
        {% endfor %}
        
        