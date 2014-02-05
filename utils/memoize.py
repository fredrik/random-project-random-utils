import logging
import functools

logger = logging.getLogger(__name__)


class memoized(object):
    """
    Decorator.
    Caches a function's return value based on the arguments given.
    Raises an exception if the arguments are not hashable.
    If called later with the same arguments, the cached value is returned
    and the function is not executed again.
    """
    def __init__(self, func):
        self.func = func
        self.cache = {}

    def __call__(self, *args):
        try:
            return self.cache[args]
        except KeyError:
            value = self.func(*args)
            self.cache[args] = value
            return value
        except TypeError:
            # unhashable -- for instance, passing a list as an argument.
            logger.exception(u'asked to memoize an uncachable set of arguments for %s. not calling function.', self.func.__name__)
            raise

    def __repr__(self):
        """Return the function's docstring."""
        return self.func.__doc__

    def __get__(self, obj, objtype):
        """Support instance methods."""
        return functools.partial(self.__call__, obj)
