from abc import ABC, abstractmethod


class BaseHandler(ABC):
    command: str

    @abstractmethod
    def answer(self, args: str | None = None) -> tuple[str, dict]:
        raise NotImplementedError
