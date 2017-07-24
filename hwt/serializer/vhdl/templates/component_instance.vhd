{{indent}}{{ instanceName }}: COMPONENT {{ entity.name }}
{% if genericMaps|length >0 %}{{indent}}    GENERIC MAP ({{genericMaps|join(',\n            ')}}
{{indent}}    )
{% endif %}{% if portMaps|length >0 %}{{indent}}    PORT MAP ({{portMaps|join(',\n            ')}}
{{indent}}    );{% endif %}
