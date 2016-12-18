{% if hasToBeVhdlProcess %}{% if sensitivityList|length>0 %}always @ ({{ sensitivityList|join(' or ') }}){% else %}always_comb
begin : {{ name }}
{%endif%}
        {% for s in statements %}
	{{s}}; 
	{% endfor %}
end{% else %}{% for s in statements %}{{s}}; {% endfor %}{% endif %}
	
