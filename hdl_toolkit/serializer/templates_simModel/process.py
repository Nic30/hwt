    @sensitivity({{sensitivityList}})
    def {{name}}(self, sim):{% for stmLine in stmLines %}
        {{ stmLine }}{% endfor %}