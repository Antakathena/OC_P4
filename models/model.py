import abc

class Model(abc.ABC):
    # @abc.abstractmethod
    # commenté car on verra plus tard
    def save(self):
        raise NotImplementedError
