from bot.core.services.EntityRepository import EntityRepository
from bot.core.models.sqlalchemy.Command import Command
from sqlalchemy.orm import Session


class CommandRepository(EntityRepository[Command]):
    def __init__(self, session: Session):
        super(CommandRepository, self).__init__()
        self._command = self.session.query(Command)

    def add(self, command: Command):
        pass

    def update(self, command: Command):
        pass

    def delete(self, command: Command):
        pass

    def get(self, command: Command):
        pass

    def exists(self, command: Command) -> bool:
        pass
