ARCHITECTURE {{ name }} OF {{ entityName }} IS
    {% for t in extraTypes %}{{t}};
    {% endfor %}
    {% for v in variables %}{{v}};    
    {% endfor %}
    {% for c in components %}{{c}}
    {% endfor %} 
BEGIN
    {% for s in statements %}{{s}};
    {% endfor %} 
    {% for c in componentInstances %}{{c}}
    {% endfor %} 
    {% for p in processes %}
    {{p}}
    {% endfor %}
END ARCHITECTURE {{ name }};
