import functools


class RoutingException(Exception):
    pass

class Router(object):

    def __init__(self, default_handler=None):
        self.table = {}
        self.default_handler = default_handler

    def register(self, path, function):
        if path in self.table:
            raise RoutingException("Path %s is being registered twice" % path)
        self.table[path] = function

    def route(self, path):
        handler = self.table.get(path, self.default_handler)
        if not handler:
            raise RoutingException("No route matched for path %s" % path)
        return handler

ROUTING_TABLE = Router()

def route(path):
    def decorator(f):
        ROUTING_TABLE.register(path, f)
        @functools.wraps(f)
        def wrapped(*args, **kwargs):
            f(*args, **kwargs)
        return wrapped
    return decorator
