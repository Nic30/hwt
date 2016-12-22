module {{ name }}{% if generics|length >0 %} # (
        {{generics|join(';\n')}}
    ){% endif %}{% if ports|length >0 %}(
        {{ports|join(',\n')}}
    );{% endif %}
    
    {% for t in extraTypes %}{{t}};
    {% endfor %}
    {% for v in variables %}{{v}};    
    {% endfor %}
    {% for c in components %}{{c}}
    {% endfor %} 
    {% for c in componentInstances %}{{c}}
    {% endfor %} 
    {% for p in processes %}{{p}}
    {% endfor %}

endmodule
