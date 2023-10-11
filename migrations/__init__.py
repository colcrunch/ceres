import abc


class AbstractMigration(abc.ABC):
    @classmethod
    @abc.abstractmethod
    def forward(cls):
        raise NotImplemented()

    @classmethod
    @abc.abstractmethod
    def backward(cls):
        raise NotImplemented()
