COMPONENT {{ entity.name }} IS
   {% if generics|length >0 %}GENERIC ( 
	{{generics|join(';\n')}} 
   );
   {% endif %}{% if port|length >0 %}PORT (
	{{port|join(';\n')}}
   );{% endif %}
END COMPONENT;
