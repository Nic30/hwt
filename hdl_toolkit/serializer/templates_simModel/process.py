    # sensitivity: {{sensitivityList|join(", ")}}
    def {{name}}(self, sim):
        __condVld = True{% for stmLine in stmLines %}
{{ stmLine }}{% endfor %}