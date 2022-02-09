from six import with_metaclass
from abc import abstractmethod, ABCMeta


class BaseOutput(with_metaclass(ABCMeta)):
    """Abstract base class for Output types"""

    def __init__(self, config, *args, **kwargs):
        self.config = config

    @abstractmethod
    def write(self, report, *args, **kwargs):
        """write report to output backend"""
        pass
