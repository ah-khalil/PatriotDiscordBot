import uuid

from abc import ABC, abstractmethod
from typing import TypeVar, Generic
from bot.core.startup import session_factory
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm.session import Session

T = TypeVar('T')


class EntityRepository(Generic[T], ABC):
    def __init__(self):
        self.session: Session = session_factory()

    @abstractmethod
    def add(self, item: T):
        pass

    @abstractmethod
    def delete(self, item: T):
        pass

    @abstractmethod
    def update(self, item: T):
        pass

    @abstractmethod
    def get(self, item: T):
        pass

    @staticmethod
    def generate_uuid():
        return uuid.uuid4().__str__()
