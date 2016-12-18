from hdl_toolkit.hdlObjects.typeShortcuts import vecT
from hdl_toolkit.hdlObjects.types.array import Array
from hdl_toolkit.hdlObjects.types.arrayVal import ArrayVal
from hdl_toolkit.hdlObjects.types.bitsConversions import convertBits__val
from hdl_toolkit.hdlObjects.types.bitsVal import BitsVal
from hdl_toolkit.hdlObjects.types.defs import BIT, SLICE
from hdl_toolkit.hdlObjects.types.enum import Enum
from hdl_toolkit.hdlObjects.specialValues import DIRECTION, SENSITIVITY
from hdl_toolkit.simulator.types.simIntConversions import convertSimInteger__val 
from hdl_toolkit.simulator.types.simInt import SIM_INT, simHInt
from hdl_toolkit.simulator.types.simBits import simBitsT
from hdl_toolkit.simulator.types.simBitsConversions import convertSimBits__val
from hdl_toolkit.simulator.simModel import (SimModel, sensitivity, connectSimPort,
                                            simEvalCond, mkUpdater, mkArrayUpdater)
from hdl_toolkit.synthesizer.codeOps import Concat
from hdl_toolkit.synthesizer.rtlLevel.netlist import RtlNetlist
from hdl_toolkit.simulator.simSignal import SimSignal
from hdl_toolkit.hdlObjects.types.sliceVal import SliceVal

{% for c in componentInstances %}
if "{{c.name}}" not in locals(): # support for all models in single file
    from {{c.name}} import {{c.name}}{% endfor %}
{% for imp in imports %}
{{imp}}
{% endfor %}

class {{ name }}(SimModel):
    _name = "{{ name }}" 
    _cntx = RtlNetlist(){% for t in extraTypes %} 
    {{t}}{% endfor %}
    
    # ports{% for name, dtype in ports %}
    {{name}} = SimSignal(_cntx, "{{name}}", {{dtype}}){% endfor %}
    
    # internal signals{% for name, dtype, defVal in signals %}
    {{name}} = SimSignal(_cntx, "{{name}}", {{dtype}}, defaultVal={{defVal}}){% endfor %}
    
{% for proc in processes %}
{{proc}}
{% endfor %}
    
    def __init__(self):
        self._interfaces = [{% for name, _ in ports   %}self.{{name}},
                            {% endfor %}{% for name, _, _ in signals %}self.{{name}},
                            {% endfor %}]
        self._processes = [{% for procName in processesNames %}self.{{procName}},
                           {% endfor %}]
        {% for c in componentInstances %}
        # connect ports{% for p in c.ports %}
        connectSimPort(self, {{c.name}},"{{p.src.name}}", "{{p.dst.name}}", {{p.direction}}){% endfor %}
        self.{{c._name}} = {{c.name}}()
        {% endfor %}
        
        self._units = [{% for c in componentInstances %}self.{{c._name}},
                       {% endfor %}
                       ]
        {% for proc in processObjects %}
        sensitivity(self.{{proc.name}}, {% 
            for s in proc.sensitivityList %}{% 
                if isOp(s) %}({{ sensitivityByOp(s.operator) }}, self.{{s.ops[0].name}}){% 
                else %}self.{{s.name}}{%
                endif %}{% 
                if not loop.last %}, {% 
                endif %}{% 
            endfor %}){% 
        endfor %}
