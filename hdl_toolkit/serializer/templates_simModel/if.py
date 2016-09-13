{{indent}}__cond, __condVldTmp = simEvalCond({{ cond }}, sim)
{{indent}}__condVld = __condVld and __condVldTmp
{{indent}}if __cond or not __condVld:{% if ifTrue %}{% for stm in ifTrue %}
{{stm}}{% endfor %}{% else %}pass{% endif %}
{{indent}}else:
{{indent}}    {% for c, stms in elIfs %}
{{indent}}    __cond, __condVldTmp = simEvalCond({{ c }}, sim)
{{indent}}    __condVld = __condVld and __condVldTmp
{{indent}}    if __cond or not __condVld:{% for stm in stms %}
{{stm}}{% endfor %}
{{indent}}        raise StopIteration(){% endfor %}
{{indent}}    {% if ifFalse %}{% for stm in ifFalse %}
{{stm}}{%endfor%}{%endif%}
