{{indent}}c_{{indentNum}}, cVld_{{ indentNum }} = simEvalCond(sim, {{ cond }})
{{indent}}#if ():
{{indent}}if c_{{indentNum}} or not cVld_{{ indentNum }}: 
{{indent}}    cVld_{{ indentNum }} = cVld_{{ indentNum-1 }} and cVld_{{ indentNum }}{%
    if ifTrue|length > 0 %}{% 
        for stm in ifTrue %}
{{stm}}{% endfor %}{% 
    else %}{% 
        if default is none 
%}{{indent}}    pass{% 
        else %}
{{indent}}    {{default}}{% 
        endif %}{% 
    endif %}{% 
    if  ifFalse|length > 0 or elIfs|length >0 %}
{{indent}}#else ():
{{indent}}if not c_{{indentNum}} or not cVld_{{ indentNum }}:{% 
        for c, stms in elIfs %}
{{indent}}    #elif ():
{{indent}}    c_{{indentNum}}, cVld_{{ indentNum }}_tmp = simEvalCond(sim, {{ c }})
{{indent}}    if c_{{indentNum}} or not cVld_{{ indentNum }}_tmp: 
{{indent}}        cVld_{{ indentNum }} = cVld_{{ indentNum }}_tmp and cVld_{{ indentNum }}
{{indent}}        cVld_{{ indentNum +1}} = cVld_{{ indentNum }}{%
              if stms|length > 0 %}{% 
                for stm in stms %}
{{stm}}{%        endfor %}{%
    else %}
{{indent}}    #default{% 
        if default is none 
%}{{indent}}    pass{% 
        else %}
{{indent}}    {{default}}{% 
        endif %}{%
    endif %}{% 
        endfor %}{% 
        if ifFalse|length > 0 %}
{{indent}}    #else:
{{indent}}    if not c_{{indentNum}} or not cVld_{{ indentNum }}:
{{indent}}        cVld_{{ indentNum +1}}  = cVld_{{ indentNum }}
        {%
            for stm in ifFalse %}
{{stm}}{%   endfor%}{%
        else %}
{{indent}}    #default{% 
        if default is none 
%}{{indent}}    pass{% 
        else %}
{{indent}}    {{default}}{% 
        endif %}{%
        endif %}{% 
    endif%}{#
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
    

########################################################################
if cond:
    ...
elif cond_1:
    ...
else:
    ...

condDefined = True
cond = cond.eval()
if cond or cond == UNKNOWN:
    condDefined_0 = condDefined and cond != UNKNOWN 
    ...

#elif
if not cond or cond == UNKNOWN:
    condDefined_0 = condDefined_0 or cond != UNKNOWN 
    cond_1 = cond_1.eval()    
    if cond_1 or cond_1 == UNKNOWN:
        condDefined_1 = condDefined_0 and cond_1 != UNKNOWN 
        ...

    
    #else
    if cond_1 == UNKNOWN or not cond_1 
        condDefined_1 = condDefined_1 or cond_1 != UNKNOWN
        ...            
#}