from functools import wraps


class Debugger:
    def __init__(self):
        self._enabled = False
        self._transport = print

    def enable(self):
        self._enabled = True

    def disable(self):
        self._enabled = False

    def set_transport(self, transport):
        self._transport = transport

    def log(self, msg, *tags):
        formatted_msg = " ".join(("PySpy", *tags)) + " : " + str(msg)
        self._transport(formatted_msg)

    def log_call(self, *tags):
        def wrapper(f):
            @wraps(f)
            def wrapped(*args, **kwargs):
                self.log("calling '%s' with args %s and kwargs %s" % (f.__name__, str(args), str(kwargs)), *tags)
                return f(*args, **kwargs)

            return wrapped

        return wrapper

    def log_return(self, *tags):
        def wrapper(f):
            @wraps(f)
            def wrapped(*args, **kwargs):
                ret = f(*args, **kwargs)
                self.log("'%s' returned %s" % (f.__name__, str(ret)), *tags)
                return ret

            return wrapped

        return wrapper

    def log_func(self, *tags):
        def wrapper(f):
            @wraps(f)
            def wrapped(*args, **kwargs):
                self.log("calling '%s' with args %s and kwargs %s" % (f.__name__, str(args), str(kwargs)), *tags)
                ret = f(*args, **kwargs)
                self.log("'%s' returned %s" % (f.__name__, str(ret)), *tags)
                return ret

            return wrapped

        return wrapper
