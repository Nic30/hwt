COMPONENT {{ entity.name }} IS
   {% if generics|length >0 %}GENERIC ( 
	{{generics|join(';\n')}} 
   );
   {% endif %}{% if ports|length >0 %}PORT (
	{{ports|join(';\n')}}
   );{% endif %}
END COMPONENT;
