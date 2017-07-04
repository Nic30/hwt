{% if hasToBeVhdlProcess %}{{indent}}{% if sensitivityList|length>0 %}always @({{ sensitivityList}}){% else %}always_comb
{%endif%} begin: {{ name }}{% for s in statements %}
{{s}};{% endfor %}
{{indent}}end{% else %}{% for s in statements %}{{s}}; {% endfor %}{% endif %}
