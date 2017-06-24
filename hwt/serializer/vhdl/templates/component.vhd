{{indent}}COMPONENT {{ entity.name }} IS
{% if generics|length >0 %}{{indent}}   GENERIC ({{generics|join(';\n            ')}}
{{indent}}   );
{% endif %}{% if ports|length >0 %}{{indent}}   PORT ({{ports|join(';\n            ')}}
{{indent}}   );{% endif %}
{{indent}}END COMPONENT;
