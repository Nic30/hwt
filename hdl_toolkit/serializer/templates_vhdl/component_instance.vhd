{{ instanceName }} : COMPONENT {{ entity.name }}
{% if genericMaps|length >0 %}GENERIC MAP ( 
	{{genericMaps|join(',\n')}} 
   )
{% endif %}{% if portMaps|length >0 %}   PORT MAP (
	{{portMaps|join(',\n')}}
   );
{% endif %}

