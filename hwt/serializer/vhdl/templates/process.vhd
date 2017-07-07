{% if hasToBeVhdlProcess %}{{indent}}{{ name }}: PROCESS {% if sensitivityList|length>0 %}({{ sensitivityList }}){% else %}--(){%endif%}{% if extraVars %}{% for v in extraVars %}
{{v}};{% endfor %}{% endif %}
{{indent}}BEGIN{% for s in statements %}
{{s}};{% endfor %}
{{indent}}END PROCESS;
{% else %}{% for s in statements %}{{s}};{% endfor %}{% endif %}
