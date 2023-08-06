import functools
import traceback


def print_exc(func):
    """
    A decorator that wraps the passed in function and prints any exceptions.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception:
            traceback.print_exc()
            raise

    return wrapper
