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
==============

Controller serve as the logic hub of the application and bridge from view and model.

The View
========

Frame: Non-interacting Frame widget.
View: interacting, requires a controller.
ViewSet: combine multiple views




Application flow
================

1. app.py, calls a controller
2. controller loads model
3. controller loads view
4. controller loads view (if necessary)

