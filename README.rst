========
Jules-tk
========

A small MVC Framework for Tkinter.

The model is Thread-safe, but since Tk is not thread safe, the view and controllers are not thread-safe.
In threaded applications; use different threads to update the model and run a polling (using view.after) to update
the view.

Design structure
================

MVC: Model-View-Controller, is a well-known and wide practiced design paradigm for designing Graphical User Interfaces (GUI's).

Jules-tk provides the MVC structure, similar to what web-frameworks as django do. There is one entry-point to the application
(app.py) which will load controllers. The controllers will then initialize the models it needs and the view it works with.

The Controller
--------------

Controller serve as the logic hub of the application and bridge from view and model.

The View
--------

* Frame: Non-interacting Frame widget.
* View: interacting, requires a controller.
* ViewSet: combine multiple views into one window.

The Model
---------

Models store and manipulate data contained by the application. They also serve as a gateway in multi-threaded
applications: Meaning, multiple threads can share information via the Model. One could - for example - use threads to
 manipulate the Model, while the View and Controller are updated in the MainThread using the Model.


Observer and Observable
=======================

The observer-observable paradigm enables objects to notify other objects upon an important change.
Models are by default observable, but Controllers need to inherit the Observer class.
See the `click_me` example for a demonstration of this paradigm.

Be aware that this paradigm is not easy to implement in multi-threaded applications. In those cases it may be better
to use a polling mechanism in the MainThread to periodically update the View.

Application flow
================

1. app.py, calls a controller
2. controller loads model
3. controller loads view
4. app.py enters mainloop
5. app.py exits mainloop
6. app.py asks controllers to stop
7. controller asks view to stop

While in the main loop

1. view receives to user input
2. view calls controller
3. controller handles input - acts on model
5. controller handles update - acts on view

Plotting
========

Basic plotting is implemented using matplotlib with the `plot.Plot` Widget.
See the `random_plot` example for a demonstration.
