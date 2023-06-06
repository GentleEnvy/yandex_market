from abc import ABC, abstractmethod


class BaseHandler(ABC):
    command: str

    @abstractmethod
    def answer(self, args: str | None, **kwargs) -> tuple[str, dict]:
        raise NotImplementedError
