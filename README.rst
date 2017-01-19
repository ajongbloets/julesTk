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
ViewSet: combine multiple views into one window

The Model
=========

Models store and handle data. These should be thread-safe, allowing for multithreaded applications to work with the GUI.
The model in those cases serves as the interface between threads.

Observer and Observable
=======================
The observer-observable paradigm is used to provide update routes between the model and the controller.


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
4. model updates - calls controller
5. controller handles update - acts on view