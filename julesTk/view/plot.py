"""Implement a Frame with a matplotlib"""

from __future__ import absolute_import
from . import *

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure


class PlotFrame(Frame):

    def __init__(self, parent):
        super(PlotFrame, self).__init__(parent)
        self._figure = None
        self._canvas = None
        self._toolbar = None
        self._legend = None
        self._axes = None

    def _setup_figure(self, size, dpi=100):
        if not isinstance(size, tuple) and not len(size) == 2:
            raise ValueError("Invalid value for size (need tuple of length 2)")
        f = Figure(figsize=size, dpi=dpi)
        self._figure = f

    def _setup_canvas(self):
        if not isinstance(self.figure, Figure):
            raise ValueError("Invalid figure object")
        self._canvas = FigureCanvasTkAgg(self.figure, self)
        self._setup_toolbar()
        self.canvas.show()
        self._canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

    def _setup_toolbar(self):
        self._toolbar = NavigationToolbar2TkAgg(self.canvas, self)
        self.toolbar.update()
        self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def _setup_subplot(self):
        self._axes = self.figure.add_subplot(111)

    @property
    def figure(self):
        """Returns the current add_plot figure of this Frame

        :rtype: matplotlib.figure.Figure
        """
        return self._figure

    @property
    def canvas(self):
        """Returns the current canvas of this frame

        :rtype: matplotlib.backends.backend_tkagg.FigureCanvasTkAgg
        """
        return self._canvas

    @property
    def axes(self):
        """Returns the current subplot in the figure

        :rtype: matplotlib.axes.Axes
        """
        return self._axes

    @property
    def legend(self):
        return self._legend

    @property
    def toolbar(self):
        return self._toolbar

    def setup(self, size=None, dpi=100):
        if size is None:
            size = (5, 5)
        self._setup_figure(size, dpi)
        self._setup_canvas()
        self._setup_subplot()

    def add_legend(self):
        if self.axes is not None:
            self._legend = self.axes.legend(loc='best')

    def draw(self):
        self.canvas.draw()

    def clear(self):
        self.figure.clear()
        self._setup_subplot()
        self.canvas.draw()


class PlotView(View):
    """ A view with a plot embedded.

    """

    def __init__(self, parent, controller):
        super(PlotView, self).__init__(parent, controller)
        self._plot = None

    @property
    def plot(self):
        """ Returns the plot frame embedded in this frame

        :rtype: julesTk.view.plot.PlotFrame
        """
        return self._plot

    def setup(self):
        self.configure_grid(self)
        self.setup_plot()

    def setup_plot(self):
        self._plot = PlotFrame(self)
        self.plot.setup()
