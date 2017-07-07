#include <systemc.h>


SC_MODULE({{name}}) {
    //interfaces{%
	for p in ports %}
    {{p}}{%
    endfor %}{%

    if signals %}

    //internal signals{%
    endif %}{%

    for s in signals %}
    {{s}}{%
    endfor %}{%

    if processes %}

    //processes inside this component{%
    endif %}{%

    for method in processes %}
{{method}}{%
	endfor %}{% if componentInstances %}

    // components inside this component
{% endif %}{%
    for c in componentInstances %}
    {{    c.name}} {{c._name}};{%
    endfor %}

    SC_CTOR({{name}}) {%
        if componentInstances %}: {%
            for c in componentInstances%}{{
                c._name}}("{{c._name}}"){%
                if not loop.last %}, {% endif %}{%
            endfor %} {%
    	endif %}{{'{'}}
    	{% for methodName, sensitivityList in processesSensitivity %}
        SC_METHOD({{methodName}});
        {% if sensitivityList
            %}sensitive << {%
            for s in sensitivityList|sort %}{{ s }}{%
               if not loop.last %} << {% endif %}{%
            endfor %};{%
         endif%}{%
     endfor %}{%

     if componentInstances %}

        // connect ports{%
     endif %}{%
     for c in componentInstances %}{%
           for p in c.ports %}
        {{     c.name}}.{%
    	        if p.direction == DIRECTION.IN %}{{p.dst.name}}({{p.src.name}}){%
                else %}{{p.src.name}}({{p.dst.name}}){%
                endif %};{%
           endfor %}{%
     endfor %}
    }
  }
};
