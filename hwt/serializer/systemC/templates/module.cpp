#include <systemc.h>
SC_MODULE({{name}}) {
	//interfaces{% for name, dtype in ports %}
	{{dtype}} {{name}};{% endfor %}

    //internal signals{% for name, dtype, defVal in signals %}
	{{dtype}} {{name}};{% endfor %}

    //processes inside this component{% for method in processes %}
{{method}}{% endfor %}


    SC_CTOR({{name}}) {
{% for method in methods %}
    SC_METHOD(do_and);
    sensitivity(self.{{method.name}}, {%
        for s in method.sensitivityList %}{%
            if isOp(s) %}({{ sensitivityByOp(s.operator) }}, self.{{s.ops[0].name}}){%
            else %}self.{{s.name}}{%
            endif %}{%
            if not loop.last %}, {%
            endif %}{%
        endfor %}){%
    endfor %}

    // connect ports
    {% for c in componentInstances %}
    {%     for p in c.ports %}
    {{          c.name}}.{%
    	        if p.direction == DIRECTION.IN %}{{p.dst.name}}({{p.src.name}}){%
                else %}{{p.src.name}}({{p.dst.name}}){%
                endif %};{%
           endfor %}{%
       endfor %}
    }
  }
};
