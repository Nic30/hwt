{{indent}}{{ entity.name }} {% if genericMaps|length >0 %}#({{genericMaps|join(',\n    ' + indent)}}
{{indent}}    ) {% endif %}{{ instanceName }}{% if portMaps|length >0 %} ({{portMaps|join(',\n    ' + indent)}}
{{indent}}    );
{% endif %}

