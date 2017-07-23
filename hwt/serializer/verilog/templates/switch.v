{{indent}}case({{ switchOn }})
{% for c in cases %}{{indent}}{% if c[0] is none %}default{% else %}{{c[0]}}{% endif %}:
{% if c[1]|length >0 %}{% for s in c[1] %}{{s}}
{% endfor %}{% endif %}{% endfor %}{{indent}}endcase
