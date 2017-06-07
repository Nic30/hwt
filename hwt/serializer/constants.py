from enum import Enum


class SERI_MODE(Enum):
    """
    Serializer mode for unit

    Modes are driving when unit should be serialized

    :cvar ALWAYS: always serialize as independent unit
    :cvar ONCE: serialize only once and all other occurrences of this unit replace with first serialized one
    :cvar PARAMS_UNIQ: serialize when params are unique, units with same params will be serialized as single unit
    :cvar EXCLUDE: exclude completely from serialization (useful for archetypes like LUT, GT, DPS block etc. which are already in vendor std. lib)
        cls.__name__ (name of class) is used for all component instances
    """
    ALWAYS = 0
    ONCE = 1
    PARAMS_UNIQ = 2
    EXCLUDE = 3
