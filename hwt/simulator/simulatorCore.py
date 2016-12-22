from simpy import Environment, Event
from simpy.events import URGENT, PENDING
from simpy.core import BoundClass, Process

class Initialize(Event):
    """Initializes a process. Only used internally by :class:`Process`.

    This event is automatically triggered when it is created.

    """
    def __init__(self, env, process, priority):
        # NOTE: The following initialization code is inlined from
        # Event.__init__() for performance reasons.
        self.env = env
        self.callbacks = [process._resume]
        self._value = None

        # The initialization events needs to be scheduled as urgent so that it
        # will be handled before interrupts. Otherwise a process whose
        # generator has not yet been started could be interrupted.
        self._ok = True
        env.schedule(self, priority)

class HdlProcess(Process):
    """
    Simulation process with optional start priority
    """
    def __init__(self, env, generator, priority=URGENT):
        """
        Original __init__ with new Initialize class
        """
        if not hasattr(generator, 'throw'):
            # Implementation note: Python implementations differ in the
            # generator types they provide. Cython adds its own generator type
            # in addition to the CPython type, which renders a type check
            # impractical. To workaround this issue, we check for attribute
            # name instead of type and optimistically assume that all objects
            # with a ``throw`` attribute are generators (the more intuitive
            # name ``__next__`` cannot be used because it was renamed from
            # ``next`` in Python 2).
            # Remove this workaround if it causes issues in production!
            raise ValueError('%s is not a generator.' % generator)

        # NOTE: The following initialization code is inlined from
        # Event.__init__() for performance reasons.
        self.env = env
        self.callbacks = []
        self._value = PENDING

        self._generator = generator

        # Schedule the start of the execution of the process.
        self._target = Initialize(env, self, priority)

class HdlEnvironmentCore(Environment):
    """
    Simpy Environment with patched processes to allow propcess start priotiry tweaks
    """
    process = BoundClass(HdlProcess)