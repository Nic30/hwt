{{indent}}if({{ cond }}) {% if ifTrue|length >0 %}{{ '{' }}
{% for s in ifTrue %}{{s}}
{%endfor%}{{indent}}end{% endif %}{% if elIfs|length >0 %}{% for c, stms in elIfs %}{{indent}}{{ '}' }} else if({{c}}) {{ '{' }}
{% for s in stms %}{{s}}
{%endfor%}{%endfor%}{{indent}}end{% endif %}{% if ifFalse|length >0 %} else {{ '{' }}
{%for s in ifFalse %}{{s}}
{% endfor %}{% endif %}{{indent}}{{ '}' }}
