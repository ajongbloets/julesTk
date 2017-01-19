"""The polling mixin for controllers (poller) helps controllers to update the view based on changes in the model"""

from julesTk.controller import Controller

__author__ = "Joeri Jongbloets <joeri@jongbloets.net>"


class Poller(Controller):
    """Poller; a polling controller"""

    def __init__(self, *args, **kwargs):
        super(Poller, self).__init__(*args, **kwargs)
        self._interval = 1  # in seconds
        self._polling = False  # whether the poller is active

    @property
    def interval(self):
        return self._interval

    @interval.setter
    def interval(self, v):
        self._interval = v

    def is_polling(self):
        return self._polling is True

    def set_polling(self, state):
        self._polling = state is True

    def setup(self):
        raise NotImplementedError

    def start(self):
        raise NotImplementedError

    def update(self, observable):
        raise NotImplementedError

    def run(self):
        """Runs the poller"""
        self.set_polling(True)
        self._update()

    def execute(self):
        raise NotImplementedError

    def _update(self):
        try:
            self.execute()
        except KeyboardInterrupt:
            self.set_polling(False)
        if self.is_polling():
            self.view.after(int(self._interval * 1000), self._update)

    def stop(self):
        self.set_polling(False)
        super(Poller, self).stop()
