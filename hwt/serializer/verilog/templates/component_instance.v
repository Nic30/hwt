{{ entity.name }} {{ instanceName }} 
{% if genericMaps|length >0 %}# ( 
	{{genericMaps|join(',\n')}} 
   )
{% endif %}{% if portMaps|length >0 %}   (
	{{portMaps|join(',\n')}}
   );
{% endif %}

