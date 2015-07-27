import kivy_overrides
import kivy.clock

_get_time = kivy.clock._default_time
_kivy_clock = kivy.clock.Clock

class _ClockEvent(object):
    def __init__(self, clock, func, event_time, repeat_interval):
        self.clock = clock
        self.func = func
        self.event_time = event_time
        self.repeat_interval = repeat_interval
        self.count = 0
        self.target_time = event_time

    def tick(self):
        now = self.clock.now()
        if now >= self.target_time:
            self.func()
            if self.repeat_interval is None:
                try:
                    self.clock._events.remove(self)
                except ValueError:
                    pass
            else:
                self.count += 1
                self.target_time = (self.event_time +
                                    self.repeat_interval * self.count)

class Clock(object):
    def __init__(self):
        self._events = []

    def now(self):
        return _get_time()

    def tick(self):
        for event in self._events[:]:
            event.tick()

    def usleep(self, usec):
        _kivy_clock.usleep(usec)

    def schedule(self, func, event_delay=None, event_time=None,
                 repeat_interval=None):
        now = self.now()
        if event_delay is not None:
            event_time = now + event_delay
        elif event_time is None:
            event_time = now
        self._events.append(
            _ClockEvent(self, func, event_time, repeat_interval))
        return func

    def unschedule(self, func):
        self._events = [event for event in self._events if event.func != func]

clock = Clock()
