{{indent}}{{ entity.name }} {{ instanceName }}{% if genericMaps|length >0 %} #({{genericMaps|join(',\n    ' + indent)}} 
{{indent}}    ){% endif %}{% if portMaps|length >0 %} ({{portMaps|join(',\n    ' + indent)}}
{{indent}}    );
{% endif %}

