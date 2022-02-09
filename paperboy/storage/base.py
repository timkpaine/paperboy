from six import with_metaclass
from abc import abstractmethod, ABCMeta


class BaseStorage(with_metaclass(ABCMeta)):
    """Abstract base class representing the interface to a storage configuration"""

    def __init__(self, config, *args, **kwargs):
        """
        Args:
            config: Paperboy application config
        """
        self.config = config

    @abstractmethod
    def status(self, *args, **kwargs):
        """Method to populate general status information in Status tab of gui"""
        pass

    @abstractmethod
    def form(self, *args, **kwargs):
        """Method to generate form on gui to create new instance.

        Returns:
            paperboy.config.forms.Response as dict
        """
        pass

    @abstractmethod
    def search(self, *args, **kwargs):
        """Method to search for instance"""
        pass

    @abstractmethod
    def list(self, *args, **kwargs):
        """Method to list all instances of type"""
        pass

    @abstractmethod
    def detail(self, *args, **kwargs):
        """Method to view detailed fields about type"""
        pass

    @abstractmethod
    def store(self, *args, **kwargs):
        """Method to save/update instance"""
        pass

    @abstractmethod
    def delete(self, *args, **kwargs):
        """Method to delete instance"""
        pass


class UserStorage(BaseStorage):
    def __init__(self, config, *args, **kwargs):
        self.config = config

    @abstractmethod
    def login(self, *args, **kwargs):
        """Handler for user login"""
        pass

    def logout(self, *args, **kwargs):
        """Handler for user logout"""
        return True


class NotebookStorage(BaseStorage):
    """Base class for Notebook storage. Notebook backends should inherit from this class"""

    pass


class JobStorage(BaseStorage):
    """Base class for Job storage. Job backends should inherit from this class"""

    pass


class ReportStorage(BaseStorage):
    """Base class for Report storage. Report backends should inherit from this class"""

    @abstractmethod
    def generate(self, *args, **kwargs):
        """Generate reports from Job instance and JSONL papermill parameters"""
        pass
