========
Jules-tk
========

A small MVC Framework for Tkinter.

The model is Thread-safe, but since Tk is not thread safe, the view and controllers are not thread-safe.
In threaded applications; use different threads to update the model and run a polling (using view.after) to update
the view.

Look at the examples for small showcases on how to use julesTk.

Design structure
================

MVC: Model-FrameView-Controller, is a well-known and wide practiced design paradigm for designing Graphical User Interfaces (GUI's).
Using a MVC approach makes writing complex applications easier as software with this approach is more modular.

Tkinter: The default GUI framework of python. Although not the most beautiful around it does not require (complex)
dependencies and is therefore very portable.

Application
-----------

The main controller is responsible for configuring the application and managing the mainloop. It also keeps track of all
controllers loaded in the application.

The Controller
--------------

A Controller serves as the logic hub of the application and as a bridge between the view and model. It is important to
understand that julesTk requires a strict one-to-one relation between controller and view! This can be an issue when
 you create dialogs in a view-only manner and providing a controller that is also used with another view.

The FrameView
--------

* Frame: Non-interacting Frame widget.
* FrameView: interacting, requires a controller.
* ViewSet: combine multiple views into one window.

The Model
---------

Models store and manipulate data contained by the application. They also serve as a gateway in multi-threaded
applications: Meaning, multiple threads can share information via the Model. One could - for example - use threads to
 manipulate the Model, while the FrameView and Controller are updated in the MainThread using the Model.


Observer and Observable
=======================

The observer-observable paradigm enables objects to notify other objects upon an important change.
Models are by default observable, but Controllers need to inherit the Observer class.
See the `click_me` example for a demonstration of this paradigm.

Be aware that this paradigm is not easy to implement in multi-threaded applications. In those cases it may be better
to use a polling mechanism in the MainThread to periodically update the FrameView.

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

1. view receives user input
2. view calls controller
3. controller handles input - acts on model
4. controller handles update - acts on view

Modals
======

Basic functionality for modal window have been implemented. These windows allow to block input to any other window
than  the modal window. This allows for the creation of Dialogs (such as alert boxes, question boxes or progress
dialogs). A basic implementation of these dialog is made in the utils subpackage.

Modal windows can be used with a MVC approach but also in a quick and dirty view-only manner. This latter is suitable
for simple dialogs.

Plotting
========

Basic plotting is implemented using matplotlib with the `plot.Plot` Widget.
See the `random_plot` example for a demonstration.


Future plans
============

* Support events
* Implement validating models/variables for dialogs (or other widgets)
