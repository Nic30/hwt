{% if hasToBeVhdlProcess %}{{ name }}: PROCESS {% if sensitivityList|length>0 %}({{ sensitivityList }}) {% else %}--(){%endif%}{% if extraVars %}{% for v in extraVars %}
        {{v}};{% endfor %}{% endif %}
    BEGIN{% for s in statements %}
	{{s}}; 
{% endfor %}END PROCESS;
{% else %}{% for s in statements %}{{s}}; {% endfor %}{% endif %}
