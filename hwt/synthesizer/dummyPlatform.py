from hwt.synthesizer.rtlLevel.extract_part_drivers import extract_part_drivers
from hwt.synthesizer.rtlLevel.mark_visibility_of_signals_and_check_drivers import markVisibilityOfSignalsAndCheckDrivers
from hwt.synthesizer.rtlLevel.remove_unconnected_signals import removeUnconnectedSignals


class DummyPlatform():
    """
    Dummy synthesis platform, base class of all chip and toolset specific platforms.
    Plaform in this context is a set of configurations which do describe the target toolset and chip/node.
    It can also contains pre/post processing callbacks and optimizations required for this target.

    :note: all processors has to be callable with only one parameter
        which is actual Unit/RtlNetlist instance
    """

    def __init__(self):
        self.beforeToRtl = []
        self.beforeToRtlImpl = []
        self.afterToRtlImpl = []

        self.beforeHdlArchGeneration = [
            extract_part_drivers,
            removeUnconnectedSignals,
            markVisibilityOfSignalsAndCheckDrivers,
        ]
        self.afterToRtl = []
