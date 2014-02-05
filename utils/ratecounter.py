import time


class RateCounter(object):
    def __init__(self, auto_recheck=True, recheck_interval=30):
        self._auto_recheck = auto_recheck
        self._interval = recheck_interval
        self.count = 0
        self.rate = 0
        self.start_time = time.time()
        self._last_recheck = self.start_time
        self._prev_count = self.count

    def on_change(self):
        if self._auto_recheck:
            if (time.time() - self._last_recheck) >= self._interval:
                self.recheck()

    def set(self, count):
        self.count = count
        self.on_change()

    def increment(self, count=1):
        self.count += count
        self.on_change()

    def recheck(self):
        now = time.time()
        elapsed = now - self._last_recheck
        increase = self.count - self._prev_count
        self.rate = increase / elapsed

        self._last_recheck = now
        self._prev_count = self.count
        self.on_recheck()

    def on_recheck(self):
        """Will be called every time rate is recalculated"""
        pass
