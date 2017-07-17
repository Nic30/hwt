import keyword


SIMMODEL_KEYWORDS = keyword.kwlist + [
    # names defined in SimModel constructor
    '_cntx',
    '_interfaces',
    '_processes',
    '_units',
    '_outputs',
    # imports
    'hwt',
    'importlib',
    'reload',
    'vecT',
    'Array',
    'ArrayVal',
    'convertBits__val',
    'BitsVal',
    'SLICE',
    'Enum'
    'DIRECTION',
    'SENSITIVITY',
    'convertSimInteger__val',
    'simHInt',
    'SIM_INT',
    'simBitsT',
    'SIM_BIT',
    'convertSimBits__val',
    'SimModel',
    'sensitivity',
    'connectSimPort',
    'simEvalCond',
    'mkUpdater',
    'mkArrayUpdater'
    'power'
    'RtlNetlist'
    'SimSignal'
    'SliceVal']
