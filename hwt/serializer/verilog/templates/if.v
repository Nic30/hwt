{{indent}}if({{ cond }}){% if ifTrue|length >0 %} begin
{% for s in ifTrue %}{{s}}
{%endfor%}{{indent}}end{% endif %}{% if elIfs|length >0 %}{% for c, stms in elIfs %} else if({{c}}) begin
{% for s in stms %}{{s}}
{%endfor%}{%endfor%}{{indent}}end{% endif %}{% if ifFalse|length >0 %} else begin
{%for s in ifFalse %}{{s}}
{% endfor %}{{indent}}end{% endif %}
