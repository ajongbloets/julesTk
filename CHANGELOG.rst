Version 0.3.4
=============

* [BUG] Fixed compatibility with python 3 (tested 3.6)
* [BUG] Fixed examples
* Implement properties for application (Application Controller) and root (tk.TK)

Version 0.3.3
=============

* Updated "progress" dialog, to a threaded version
* Introduce states for views and controllers (is_showing, is_running, etc.)

Version 0.3.1
=============

* New "console" widget, to use as stream output for logging
* New "progress" dialog

Version 0.3.0.alpha
===================

* Implement a basic hook system for application wide events
* Implement window and modal windows
* Abstract setup/start/stop methods renamed to _prepare/_start/_stop
* Window and Application hook into "WM_DELETE_WINDOW" event
* Restructured views
* Restructured controller

Version 0.2.2
=============

* Streamline app run/start/stop method names
* Parent chaining of controllers and views
* Use functools with decorators
* Exception safe locking
* Improve docstrings

Version 0.2.1
=============

* Untangle controller classes from observer
* Move observer-observable to utils
* Add 'has_model' to controller

Version 0.2.0.alpha
===================

* Implement plotting (using matplotlib)
* Add a Gaussian Random Number generating Model
* Implement a controller with polling capabilities

Version 0.1.0.alpha
===================

* Simple MVC
* FrameView, ViewSet implementations
* Observer - Observable
* Dynamic registration of widgets and variables
