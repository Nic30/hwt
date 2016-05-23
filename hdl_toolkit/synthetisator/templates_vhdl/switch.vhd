CASE {{ switchOn }} IS
    {% for c in cases %}WHEN {% if c[0] is none %}OTHERS{% else %}{{c[0]}}{% endif %} =>
    {% if c[1]|length >0 %}{% for s in c[1] %}{{s}};
{% endfor %}{% endif %}{% endfor %}END CASE;
