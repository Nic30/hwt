{{indent}}c_{{indentNum}}, cVld_{{ indentNum }} = simEvalCond(sim, {{ cond }})
{{indent}}#if ():
{{indent}}if c_{{indentNum}} or not cVld_{{ indentNum }}: 
{{indent}}    cVld_{{ indentNum }} = cVld_{{ indentNum-1 }} and cVld_{{ indentNum }}{%
if ifTrue|length > 0 %}{% 
    for stm in ifTrue %}
{{stm}}{% 
    endfor %}{% 
else %}
{{indent}}    #enclosure
{{enclosure}}{%
endif %}
{{indent}}#else:
{{indent}}if not c_{{indentNum}} or not cVld_{{ indentNum }}:{% 
if ifFalse|length > 0 %}{%
    for stm in ifFalse %}
{{stm}}{%
    endfor%}{% 
else %}
{{indent}}    #enclosure
{{enclosure}}
{% endif %}
{#
""" This template constructs if-else trees like this """ 
if cond:
    ...
else:
    ...
    
condDefined = True
cond = cond.eval()
# if cond:
if cond or cond == UNKNOWN:
    condDefined_0 = condDefined and cond != UNKNOWN  
    ...
# else:
if not cond or cond == UNKNOWN:
    condDefined_0 = condDefined_0 or cond != UNKNOWN
    ...
#}