class ValueWidthRequirementScope():
    """
    Context manager which temporarily swaps the _valueWidthRequired on specified context 

    .. code-block:: python

        with ValueWidthRequirementScope(ctx, True):
            #...
    """

    def __init__(self, ctx, val):
        self.ctx = ctx
        self.val = val

    def __enter__(self):
        self.orig = self.ctx._valueWidthRequired
        self.ctx._valueWidthRequired = self.val

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.ctx._valueWidthRequired = self.orig
