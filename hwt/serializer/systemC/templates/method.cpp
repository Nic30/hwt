{{indent}}void {{name}}() {{ '{' }}{% for stm in statements %}
{{stm}}{% endfor %}
{{indent}}{{ '}' }}
