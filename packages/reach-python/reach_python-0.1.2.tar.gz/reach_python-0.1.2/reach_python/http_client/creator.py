from abc import abstractmethod, ABC


class HTTPClient(ABC):
    @abstractmethod
    def get(self, url: str, params: dict = None) -> dict:
        pass

    @abstractmethod
    def post(self, url: str, data: dict = None) -> dict:
        pass

    @abstractmethod
    def put(self, url: str, data: dict = None) -> dict:
        pass

    @abstractmethod
    def delete(self, url: str) -> dict:
        pass
