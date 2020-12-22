from hwt.synthesizer.rtlLevel.extract_part_drivers import extract_part_drivers
from hwt.synthesizer.rtlLevel.remove_unconnected_signals import removeUnconnectedSignals
from hwt.synthesizer.rtlLevel.mark_visibility_of_signals_and_check_drivers import markVisibilityOfSignalsAndCheckDrivers


class DummyPlatform():
    """
    :note: all processors has to be callable with only one parameter
        which is actual Unit/RtlNetlist instance
    """

    def __init__(self):
        self.beforeToRtl = []
        self.beforeToRtlImpl = []
        self.afterToRtlImpl = []

        self.beforeHdlArchGeneration = [
            removeUnconnectedSignals,
            markVisibilityOfSignalsAndCheckDrivers,
            extract_part_drivers,
        ]
        self.afterToRtl = []
