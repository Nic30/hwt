from hwt.hdlObjects.typeShortcuts import vecT
from hwt.hdlObjects.types.array import Array
from hwt.hdlObjects.types.arrayVal import ArrayVal
from hwt.hdlObjects.types.bitsConversions import convertBits__val
from hwt.hdlObjects.types.bitsVal import BitsVal
from hwt.hdlObjects.types.defs import BIT, SLICE
from hwt.hdlObjects.types.enum import Enum
from hwt.hdlObjects.constants import DIRECTION, SENSITIVITY
from hwt.simulator.types.simIntConversions import convertSimInteger__val 
from hwt.simulator.types.simInt import SIM_INT, simHInt
from hwt.simulator.types.simBits import simBitsT
from hwt.simulator.types.simBitsConversions import convertSimBits__val
from hwt.simulator.simModel import (SimModel, sensitivity, connectSimPort,
                                            simEvalCond, mkUpdater, mkArrayUpdater)
from hwt.code import Concat, power
from hwt.synthesizer.rtlLevel.netlist import RtlNetlist
from hwt.simulator.simSignal import SimSignal
from hwt.hdlObjects.types.sliceVal import SliceVal

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
