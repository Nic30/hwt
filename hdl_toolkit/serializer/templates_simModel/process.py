    # sensitivity: {{sensitivityList|join(", ")}}
    def {{name}}(self, sim):
        _condVld = True{% for stmLine in stmLines %}
{{ stmLine }}{% endfor %}