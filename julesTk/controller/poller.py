"""The polling mixin for controllers (poller) helps controllers to update the view based on changes in the model"""

from julesTk.controller import BaseController

__author__ = "Joeri Jongbloets <joeri@jongbloets.net>"


class Poller(BaseController):
    """A controller that does something at a given interval"""

    def __init__(self, parent, *args, **kwargs):
        super(Poller, self).__init__(parent)
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

    def _prepare(self):
        return True

    def _start(self):
        if not self.is_polling():
            # enable polling
            self.set_polling(True)
            # start execution of poller
            self._update()

    def execute(self):
        raise NotImplementedError

    def _update(self):
        if self.is_polling():
            try:
                self.execute()
            except KeyboardInterrupt:
                self.set_polling(False)
            self.root.after(int(self._interval * 1000), self._update)

    def _stop(self):
        if self.is_polling():
            self.set_polling(False)


class ModelUpdatePoller(Poller):

    def __init__(self, parent, model):
        super(ModelUpdatePoller, self).__init__(parent)
        self._model = model

    def get_model(self):
        """The model to be updated

        :rtype: julesTk.model.Model
        """
        return self._model

    @property
    def model(self):
        return self.get_model()

    def set_model(self, model):
        from julesTk.model import Model
        if model is not None and not isinstance(model, Model):
            raise ValueError("Invalid Model Object, expected None or a julesTk.model.Model")
        self._model = model

    def execute(self):
        self.model.update()
