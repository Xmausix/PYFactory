import time


class AutoSave:
    def __init__(self, interval: float = 120.0):
        self.interval      = interval
        self._timer        = 0.0
        self.last_save_msg = ""

    def update(self, dt: float, save_fn) -> bool:
        self._timer += dt
        if self._timer >= self.interval:
            self._timer = 0.0
            save_fn()
            self.last_save_msg = f"AutoSaved {time.strftime('%H:%M:%S')}"
            return True
        return False

    @property
    def time_until(self) -> float:
        return max(0.0, self.interval - self._timer)