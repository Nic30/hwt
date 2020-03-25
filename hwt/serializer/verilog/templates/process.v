{% if hasToBeProcess 
   %}{{indent}}{% 
    if sensitivityList|length>0 
         %}always @({{ sensitivityList}}){% 
    else %}always @(*){%  endif%} begin: {{ name }}{% 
    if extraVars %}{%
        for ev in extraVars%}
{{           indent}}{{ev}};{%      endfor%}{% 
    endif %}{% 
    for s in statements %}
{{       s}}{% 
    endfor %}
{{  indent}}end
{% else %}{% 
    if extraVars %}{%
        for ev in extraVars%}
{{            ev}};
{%      endfor%}{% 
    endif %}{%
    for s in statements
       %}{{s}}{% 
    endfor %}{% 
 endif %}
