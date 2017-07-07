{{indent}}module {{ name }}{% if generics|length >0 %} #({{generics|join(',\n'+ indent + '        ')}}
{{indent}}    ){% endif %}{% if ports|length >0 %}({{ports|join(',\n' + indent + '        ')}}
{{indent}}    );{% endif %}

