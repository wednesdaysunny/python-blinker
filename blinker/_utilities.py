from weakref import ref

from blinker._saferef import BoundMethodWeakref


try:
    callable
except NameError:
    def callable(object):
        return hasattr(object, '__call__')


class _symbol(object):

    def __init__(self, name):
        """Construct a new named symbol."""
        self.__name__ = self.name = name

    def __reduce__(self):
        return symbol, (self.name,)

    def __repr__(self):
        return self.name
_symbol.__name__ = 'symbol'


class symbol(object):
    """A constant symbol.

    >>> symbol('foo') is symbol('foo')
    True
    >>> symbol('foo')
    foo

    A slight refinement of the MAGICCOOKIE=object() pattern.  The primary
    advantage of symbol() is its repr().  They are also singletons.

    Repeated calls of symbol('name') will all return the same instance.

    """
    symbols = {}

    def __new__(cls, name):
        try:
            return cls.symbols[name]
        except KeyError:
            return cls.symbols.setdefault(name, _symbol(name))


def hashable_identity(obj):
    if hasattr(obj, 'im_func'):
        return (id(obj.im_func), id(obj.im_self))
    else:
        return id(obj)


WeakTypes = (ref, BoundMethodWeakref)


class annotatable_weakref(ref):
    """A weakref.ref that supports custom instance attributes."""


def reference(object, callback=None, **annotations):
    """Return an annotated weak ref."""
    if callable(object):
        weak = callable_reference(object, callback)
    else:
        weak = annotatable_weakref(object, callback)
    for key, value in annotations.items():
        setattr(weak, key, value)
    return weak


def callable_reference(object, callback=None):
    """Return an annotated weak ref, supporting bound instance methods."""
    if hasattr(object, 'im_self') and object.im_self is not None:
        return BoundMethodWeakref(target=object, on_delete=callback)
    return annotatable_weakref(object, callback)
