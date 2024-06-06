from typing import List

from hwt.synthesizer.rtlLevel.extract_part_drivers import RtlNetlistPassExtractPartDrivers
from hwt.synthesizer.rtlLevel.mark_visibility_of_signals_and_check_drivers import RtlNetlistPassMarkVisibilityOfSignalsAndCheckDrivers
from hwt.synthesizer.rtlLevel.remove_unconnected_signals import RtlNetlistPassRemoveUnconnectedSignals
from hwt.synthesizer.rtlLevel.rtlNetlistPass import RtlNetlistPass


class DummyPlatform():
    """
    Dummy synthesis platform, base class of all chip and toolset specific platforms.
    Platform in this context is a set of configurations which do describe the target toolset and chip/node.
    It can also contains pre/post processing callbacks and optimizations required for this target.

    :note: all processors has to be callable with only one parameter
        which is actual HwModule/RtlNetlist instance
    """

    def __init__(self):
        self.beforeToRtl = []
        self.beforeToRtlImpl = []
        self.afterToRtlImpl = []

        self.beforeHdlArchGeneration: List[RtlNetlistPass] = [
            RtlNetlistPassExtractPartDrivers(),
            RtlNetlistPassRemoveUnconnectedSignals(),
            RtlNetlistPassMarkVisibilityOfSignalsAndCheckDrivers(),
        ]
        self.afterToRtl = []
