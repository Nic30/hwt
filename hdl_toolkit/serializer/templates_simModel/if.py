{{indent}}_cond, _condVldTmp = simEvalCond(sim, {{ cond }})
{{indent}}_condVld = _condVld and _condVldTmp
{{indent}}if _cond or not _condVld:{% if ifTrue|length > 0 %}{% for stm in ifTrue %}
{{stm}}{% endfor %}{% else %}pass{% endif %}{% if  ifFalse|length > 0 or elIfs|length >0 %}
{{indent}}else:{% for c, stms in elIfs %}
{{indent}}    _cond, _condVldTmp = simEvalCond(sim, {{ c }})
{{indent}}    _condVld = _condVld and _condVldTmp
{{indent}}    if _cond or not _condVld:{% for stm in stms %}
{{stm}}{% endfor %}
{{indent}}        raise StopIteration(){% endfor %}{% if ifFalse|length > 0 %}{% for stm in ifFalse %}
{{stm}}{%endfor%}
{{indent}}    raise StopIteration(){%endif%}{%endif%}
