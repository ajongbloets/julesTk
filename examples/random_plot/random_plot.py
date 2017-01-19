"""The Random Plot Application plots random y-values using random generator"""
from julesTk import app, view
from julesTk.controller.poller import Poller
from julesTk.model.random import RandomModel
from julesTk.view.plot import PlotFrame

__author__ = "Joeri Jongbloets <joeri@jongbloets.net>"


class RandomPlotApp(app.Application):

    def __init__(self):
        super(RandomPlotApp, self).__init__()

    def setup(self):
        c = MainController(self).setup()
        self.add_controller("main", c)

    def run(self):
        self.get_controller("main").start()


class MainController(Poller):

    def setup(self):
        if self.view is None:
            self._view = MainView(self.application, self)
        if self.model is None:
            self.model = RandomModel()
            self.model.register_observer(self)
        self.view.setup()
        return self

    @property
    def view(self):
        """ Return the view managed by this controller

        :rtype: MainView
        """
        return super(MainController, self).view

    def start(self):
        self.view.show()

    def execute(self):
        """Executed every x seconds"""
        self.model.update()

    def stop(self):
        self.view.close()

    def update(self, observable):
        if isinstance(observable, RandomModel):
            self.update_plot()

    def update_plot(self):
        plt = self.view.plot
        # initialize
        plt.clear()
        data = self.model.data[:]
        if len(data) > 0:
            # now plot
            plt.axes.plot(range(len(data)), data)
        plt.draw()

    def start_poller(self):
        self.set_polling(True)
        self.run()

    def stop_poller(self):
        self.set_polling(False)

    def reset(self):
        self.model.reset()


class MainView(view.View):

    REFRESH_RATES = {
        "50 msec": 0.05,
        "100 msec": 0.1,
        "200 msec": 0.2,
        "500 msec": 0.5,
        "1 sec": 1,
        "2 sec": 2,
        "5 sec": 5,
        "10 sec": 10,
        "15 sec": 15,
        "30 sec": 30,
        "1 min": 60,
        "5 min": 300,
        "10 min": 600,
        "30 min": 1800,
        "1 hour": 3600,
    }  # in seconds per update

    def __init__(self, parent, controller):
        super(MainView, self).__init__(parent, controller)
        self._plot = None

    def setup(self):
        self.grid(sticky="nsew")
        self.configure_column(self, [0, 1, 2])
        self.configure_row(self, [0, 1, 2])
        self.configure_row(self.parent, 0)
        self.configure_column(self.parent, 0)
        # add start button
        startbtn = view.ttk.Button(self, text="Start", command=self.start_clicked)
        self.add_widget("start", startbtn)
        startbtn.grid(row=0, column=0)
        # add pause button
        pausebtn = view.ttk.Button(self, text="Pause", command=self.pause_clicked, state="disabled")
        self.add_widget("pause", pausebtn)
        pausebtn.grid(row=0, column=1)
        # add reset button
        resetbtn = view.ttk.Button(self, text="Reset", command=self.controller.reset)
        self.add_widget("reset", resetbtn)
        resetbtn.grid(row=0, column=2)
        # add refresh rate picker
        lbl = view.ttk.Label(self, text="Refresh every")
        lbl.grid(row=1, column=0)
        refresh_var = self.add_variable("refresh", view.tk.StringVar())
        refresh = view.ttk.Combobox(self, textvariable=refresh_var, state="readonly")
        rates = sorted(self.REFRESH_RATES.keys(), key=self.REFRESH_RATES.get)
        refresh["values"] = rates
        refresh.current(rates.index("1 sec"))
        refresh.bind("<<ComboboxSelected>>", self.update_rate)
        refresh.grid(row=1, column=1, columnspan=2)
        if self._plot is None:
            self._plot = PlotFrame(self)
        self.plot.setup()
        self.plot.grid(sticky="nsew", row=2, column=0, columnspan=3)

    @property
    def plot(self):
        """ Return the plot embedded in this view

        :rtype: julesTk.view.plot.PlotFrame
        """
        return self._plot

    @property
    def refresh_rate(self):
        v = self.get_variable("refresh").get()
        return float(self.REFRESH_RATES.get(v, 1))

    def start_clicked(self):
        self.get_widget("start")["state"] = "disabled"
        self.get_widget("pause")["state"] = "normal"
        self.controller.start_poller()

    def pause_clicked(self):
        self.get_widget("pause")["state"] = "disabled"
        self.get_widget("start")["state"] = "normal"
        self.controller.stop_poller()

    def update_rate(self, event):
        self.controller.interval = self.refresh_rate

if __name__ == "__main__":

    app = RandomPlotApp()
    app.start()
