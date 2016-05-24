IF {{ cond }} THEN{% if ifTrue|length >0 %}
    {% for s in ifTrue %}{{s}};
    {%endfor%}{% endif %}{% if elIfs|length >0 %}{% for c, stms in elIfs %}elsif {{c}}
        {% for s in stms %}{{s}};
    {%endfor%}{%endfor%}{% endif %}{% if ifFalse|length >0 %}ELSE
    {%for s in ifFalse %}{{s}};
{% endfor %}{% endif %}END IF
