import inspect
from flask import abort


__all__ = ['validate']


def validate(*__validators__):
    for __validator__ in __validators__:
        if not inspect.isclass(__validator__):
            raise TypeError('The validate decorator only accepts class.')
        method = getattr(__validator__, 'validate', None)
        if method is None or not callable(method):
            raise AttributeError('The validator should contains a callable method "validate(self)"')

    def decorator(func):

        def func_wrapper(*args, **kwargs):
            for __validator__ in __validators__:
                if not __validator__().validate():
                    abort(400)
            return func(*args, **kwargs)

        return func_wrapper

    return decorator
