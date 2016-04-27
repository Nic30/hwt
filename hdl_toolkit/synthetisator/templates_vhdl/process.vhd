{% if hasCond %}{{ name }}: PROCESS {% if sensitivityList|length>0 %}({{ sensitivityList }}){% else %}--(){%endif%}
BEGIN{% for s in statements %}
	{{s}}; 
	{% endfor %}
END PROCESS;{% else %}{% for s in statements %}{{s}}; {% endfor %}{% endif %}
	
