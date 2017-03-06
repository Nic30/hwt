from random import Random


def valueHasChanged(valA, valB):
    return valA.val is not valB.val or valA.vldMask != valB.vldMask


def agent_randomize(agent, timeQuantum, seed):
    random = Random(seed)

    def randomEnProc(simulator):
        # small space at start to modify agents when they are inactive
        yield simulator.wait(timeQuantum / 4)
        while True:
            agent.enable = random.random() < 0.5
            delay = int(random.random() * timeQuantum)
            yield simulator.wait(delay)

    return randomEnProc
