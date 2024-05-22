from enum import Enum


class SignalDriverErrType(Enum):
    (
        MISSING_DRIVER,
        MULTIPLE_COMB_DRIVERS,
        OUTPUT_WITHOUT_DRIVER,
        INPUT_WITH_DRIVER
    ) = range(4)


SignalDriverErrType_labels = {
    SignalDriverErrType.MISSING_DRIVER: "  missing driver for:",
    SignalDriverErrType.MULTIPLE_COMB_DRIVERS: "  multiple comb. drivers for:",
    SignalDriverErrType.OUTPUT_WITHOUT_DRIVER: "  outputs without driver:",
    SignalDriverErrType.INPUT_WITH_DRIVER: "  inputs with driver:",
}


class SignalDriverErr(Exception):
    """
    Signal has multiple combinational drivers (this is not possible in real word)
    or signal has no driver specified and it drives something which has effect on any output of component
    (it needs to have a driver but it does not have one)

    :note: SignalDriverErr([(SignalDriverErrType, sig), ])
    """

    def __str__(self):
        try:
            ctx = self.args[0][0][1].ctx
            name = ctx.getDebugScopeName()
            scope_name = f"{name:s} of class {ctx.parent.__class__}"
        except Exception:
            scope_name = "<no parent>"

        b = [f"{self.__class__} raised in {scope_name:s}"]
        err_sigs = sorted(self.args[0], key=lambda x: (x[0].value, x[1].name))
        prev_err_t = None
        for err_t, sig in err_sigs:
            if prev_err_t is None or prev_err_t != err_t:
                b.append(SignalDriverErrType_labels[err_t])
                prev_err_t = err_t
            if err_t == SignalDriverErrType.MULTIPLE_COMB_DRIVERS or\
                    err_t == SignalDriverErrType.INPUT_WITH_DRIVER:
                b.append(f"    {sig}: {sig.drivers}")
            else:
                b.append(f"    {sig}")

        return "\n".join(b)
