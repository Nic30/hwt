ARCHITECTURE {{ name }} OF {{ entityName }} IS
    {% for t in extraTypes %}
    {{t}}
    {% endfor %}

    {% for v in variables %}
    {{v}}    
    {% endfor %}
BEGIN
    {% for p in processes %}
    {{p}}
    {% endfor %}

    {% for c in components %}
    {{c}}
    {% endfor %}      
END ARCHITECTURE_NAME;
