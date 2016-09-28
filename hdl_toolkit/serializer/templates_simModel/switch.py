{% for c in cases %}{{indent}}{% if c[0] is not none %}_cond, _condVldTmp = simEvalCond(sim, {{ switchOn }}._eq({{c[0]}}))
{{indent}}_condVld = _condVld and _condVldTmp
{{indent}}if _cond or not _condVld:{% for stm in c[1] %}
{{stm}}{% endfor %}
{{indent}}    raise StopIteration()
{% else %}{% for stm in c[1] %}
{{stm}}{% endfor %}
{%endif%}{% endfor %}
