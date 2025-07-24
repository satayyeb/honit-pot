from abc import ABCMeta


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class SingletonABCMeta(SingletonMeta, ABCMeta):
    """
    A combined metaclass that inherits from SingletonMeta and ABCMeta.
    The order here is important: SingletonMeta comes first to ensure its
    __call__ method (singleton behavior) is used.
    """
    pass
