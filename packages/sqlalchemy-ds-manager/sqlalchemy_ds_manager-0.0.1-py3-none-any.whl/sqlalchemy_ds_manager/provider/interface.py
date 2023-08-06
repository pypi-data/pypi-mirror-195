import abc

class ProviderInterface(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'new') and 
                callable(subclass.new) or 
                NotImplemented)

    @abc.abstractmethod
    def __init__(self, config: dict, uid: str, pwd: str):
        raise NotImplementedError

    @abc.abstractmethod
    def new(self):
        raise NotImplementedError