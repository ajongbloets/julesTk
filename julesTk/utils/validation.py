"""Validation Framework for widgets like Entry widgets

Based on http://effbot.org/zone/tkinter-entry-validate.htm

"""

from julesTk import view
__all__ = [
    "ValidatingWidget", "ValidatingEntry",
    "Validator", "IntegerValidator", "FloatValidator", "RangeValidator", "DateValidator"
]


class ValidatingWidget(object):
    """base object interface: defines validate as method"""

    def __init__(self, value=None, validator=None, **kwargs):
        super(ValidatingWidget, self).__init__()
        # keeps track of correct value
        self._value = value
        # keeps track of actual value
        self._variable = view.tk.StringVar()
        self._variable.set(self._value)
        # validator used to validate value
        self._validator = validator
        self._variable.trace("w", self._callback)

    def _callback(self, *dummy):
        """Checks input upon change"""
        value = self._variable.get()
        newvalue = self._validate(value)
        if newvalue is None:
            self._variable.set(self._value)
        elif newvalue != value:
            self._value = newvalue
            self._variable.set(newvalue)
        else:
            self._value = value

    def _validate(self, value):
        if self._validator is not None:
            value = self._validator.validate(value)
        return self.validate(value)

    def validate(self, value):
        return value

    @property
    def value(self):
        return self._value

    @property
    def validator(self):
        return self._validator


class ValidatingEntry(ValidatingWidget, view.ttk.Entry):

    def __init__(self, master, value=None, validator=None, **kwargs):
        ValidatingWidget.__init__(self, value=value, validator=validator)
        view.tk.Entry.__init__(self, master=master, **kwargs)
        self.configure(textvariable=self._variable)


class Validator(object):
    """base validator object"""

    def validate(self, value):
        return value


class IntegerValidator(Validator):

    def validate(self, value):
        result = None
        try:
            result = int(value)
        except (ValueError, TypeError):
            pass
        return result


class FloatValidator(Validator):

    def validate(self, value):
        result = None
        try:
            result = float(value)
        except (ValueError, TypeError):
            pass
        return result


class RangeValidator(Validator):

    def __init__(self, minimum=None, include_minimum=True, maximum=None, include_maximum=None):
        self._minimum = minimum
        self._include_minimum = include_minimum
        self._maximum = maximum
        self._include_maximum = include_maximum

    def validate(self, value):
        result = False
        above_min = True
        if self._minimum is not None:
            above_min = self._minimum < value or (self._include_minimum and self._minimum <= value)
        below_max = True
        if self._maximum is not None:
            below_max = self._maximum > value or (self._include_maximum and self._maximum >= value)
        if above_min and below_max:
            result = value
        return result


class DateValidator(Validator):

    def __init__(self, date_fmt="%Y-%m-%d"):
        self._date_fmt = date_fmt

    def validate(self, value):
        result = None
        from datetime import datetime as dt
        try:
            dt.strptime(value, self._date_fmt)
        except (TypeError, ValueError):
            pass
        return result
