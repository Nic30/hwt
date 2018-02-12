import keyword


SIMMODEL_KEYWORDS = keyword.kwlist + [
    # names defined in SimModel constructor
    '_ctx',
    '_interfaces',
    '_processes',
    '_units',
    '_outputs',
    # imports
    'hwt',
    'importlib',
    'reload',
    'HArray',
    'HArrayVal',
    'convertBits__val',
    'BitsVal',
    'SLICE',
    'HEnum'
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
