library IEEE;
use IEEE.std_logic_1164.all;
use IEEE.numeric_std.all;

{{indent}}ENTITY {{ name }} IS
{% if generics|length >0 %}{{indent}}    GENERIC ( 
	{{generics|join(';\n        ')}} 
{{indent}}    );
{% endif %}{% if ports|length >0 %}{{indent}}    PORT ({{ports|join(';\n        ')}}
{{indent}}    );{% endif %}
{{indent}}END {{ name }};

