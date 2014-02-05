class OfType(object):
    """Helper object that compares equal if other object has given type"""
    def __init__(self, t):
        self.t = t

    def __eq__(self, other):
        return type(other) == self.t