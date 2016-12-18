library IEEE;
use IEEE.std_logic_1164.all;
use IEEE.numeric_std.all;

ENTITY {{ name }} IS
{% if generics|length >0 %}  GENERIC ( 
	{{generics|join(';\n')}} 
   );
{% endif %}{% if ports|length >0 %}PORT ({{ports|join(';\n')}}
   );{% endif %}
END {{ name }};

