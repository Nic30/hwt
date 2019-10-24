import keyword


SIMMODEL_KEYWORDS = keyword.kwlist + [
    # names defined in SimModel constructor
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
    'BIT',
    'BasicRtlSimModel',
    'BasicRtlSimProxy',
    'sensitivity',
    'connectSimPort',
    'sim_eval_cond',
    'mkUpdater',
    'mkArrayUpdater',
    'slice',
    'SliceVal']
