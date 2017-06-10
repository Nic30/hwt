{% for t in extraTypes %}{{t}};
{% endfor %}{% for v in variables %}{{v}};    
{% endfor %}{% for c in components %}{{c}}
{% endfor %}{% for c in componentInstances %}{{c}}
{% endfor %}{% for p in processes %}{{p}}
{% endfor %}
{{indent}}endmodule
