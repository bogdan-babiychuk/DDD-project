from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class BaseBroker(ABC):

    @abstractmethod
    def publish(self, key:bytes, topic:str, value: bytes):
        raise NotImplementedError()

