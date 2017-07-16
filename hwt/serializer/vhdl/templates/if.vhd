{{indent}}IF {{ cond }} THEN{% if ifTrue|length >0 %}
{% for s in ifTrue %}{{s}};
{%endfor%}{% endif %}{% if elIfs|length >0 %}{% for c, stms in elIfs %}{{indent}}ELSIF {{c}} THEN
{% for s in stms %}{{s}};
{%endfor%}{%endfor%}{% endif %}{% if ifFalse|length >0 %}{{indent}}ELSE
{%for s in ifFalse %}{{s}};
{% endfor %}{% endif %}{{indent}}END IF
