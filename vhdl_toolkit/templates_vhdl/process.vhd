{{ name }}: PROCESS ({{ sensitivityList }})
BEGIN
    {% for s in statements %}
    {{str(s)}}
    {% endfor %} 
END PROCESS;
