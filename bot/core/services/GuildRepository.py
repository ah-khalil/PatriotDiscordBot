import abc
from typing import TypeVar, Generic

from bot.core.services.EntityRepository import EntityRepository
from bot.core.models.sqlalchemy.DiscordServer import DiscordServer
from sqlalchemy.orm import Session


class GuildRepository(EntityRepository[DiscordServer]):
    def __init__(self):
        super(GuildRepository, self).__init__()
        self._guild = self.session.query(DiscordServer)

    def add(self, discord_server: DiscordServer):
        pass

    def update(self, discord_server: DiscordServer):
        pass

    def delete(self, discord_server: DiscordServer):
        pass

    def get(self, discord_server: DiscordServer):
        pass

    def exists(self, discord_server: DiscordServer) -> bool:
        pass
