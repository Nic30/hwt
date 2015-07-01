

class Assigment():
    def __init__(self, src, dst):
        self.src = src
        self.dst = dst
        
    def __str__(self):
        t = self.dst.var_type.str.lower() 
        if t == 'std_logic':
            return "%s <= '%d';" % (self.dst.name, int(self.src))
        elif t.startswith("std_logic_vector"):
            return "%s <= std_logic_vector(to_unsigned(%d, %s'length));" % (self.dst.name, int(self.src), self.dst.name)
        else:
            raise Exception() 
