from abc import ABC, abstractmethod

class BaseRequestProvider(ABC):
    @abstractmethod
    def get_request(self):
        """Return a single request"""
        pass

    @abstractmethod
    def load_requests(self):
        """Load requests from the source"""
        pass
