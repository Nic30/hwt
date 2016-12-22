from enum import Enum

class SERI_MODE(Enum):
    """
    Serializer mode for unit
    
    Modes are driving when unit should be serialized
    """
    
    # always serialize as independent unit
    ALWAYS = 0 
    
    # serialize only once and all other occurrences of this unit replace with first serialized one
    ONCE = 1 
    
    # serialize when params are unique, units with same params will be serialized as single unit
    PARAMS_UNIQ = 2 
    
    # exclude completely from serialization (useful for archetypes like LUT, GT, DPS block etc. which are already in vendor std. lib)
    # cls.__name__ (name of class) is used for all component instances
    EXCLUDE = 3