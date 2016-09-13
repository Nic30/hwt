{% for c in cases %}{{indent}}{% if c[0] is not none %}__cond, __condVldTmp = simEvalCond([{{ switchOn }}._eq({{c[0]}})], sim)
{{indent}}__condVld = __condVld and __condVldTmp
{{indent}}if __cond or not __condVld:{% for stm in c[1] %}
{{stm}}{% endfor %}
{{indent}}    raise StopIteration()
{% else %}{% for stm in c[1] %}
{{stm}}{% endfor %}
{%endif%}{% endfor %}
