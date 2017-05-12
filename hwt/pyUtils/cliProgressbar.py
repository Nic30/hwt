import sys
import time


class CliProgressbar(object):
    def __init__(self, step=0.001):
        self.barLength = 40
        self.lastVal = -1
        self.step = step
        self.start = time.time()

    def update(self, progress):
        if isinstance(progress, int):
            progress = float(progress)
        if not isinstance(progress, float):
            raise TypeError()
        if progress < 0:
            progress = 0
        if progress >= 1:
            progress = 1
        if self.lastVal - progress < -self.step:
            self.lastVal = progress
            self.render(progress)

    @staticmethod
    def prettyTimeDelta(_seconds):
        seconds = int(_seconds)
        days, seconds = divmod(seconds, 86400)
        hours, seconds = divmod(seconds, 3600)
        minutes, seconds = divmod(seconds, 60)
        if days > 0:
            return '%dd%dh%dm%ds' % (days, hours, minutes, seconds)
        elif hours > 0:
            return '%dh%dm%ds' % (hours, minutes, seconds)
        elif minutes > 0:
            return '%dm%ds' % (minutes, seconds)
        elif seconds > 5:
            return '%ds' % (seconds,)
        else:
            return '%dms' % (int(_seconds * 1000))

    def render(self, progress):
        barLength = self.barLength
        block = int(round(barLength * progress))

        done = time.time()
        elapsed = done - self.start

        text = "\r[{}] {: .2f}%, {}".format("="*block + " "*(barLength - block),
                                              progress * 100,
                                              self.prettyTimeDelta(elapsed))
        sys.stdout.write(text)
        if progress == 1:
            sys.stdout.write('\n')
        sys.stdout.flush()