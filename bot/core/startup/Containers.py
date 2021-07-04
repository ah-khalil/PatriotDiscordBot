from sqlalchemy.orm import Session, sessionmaker

from bot.core.startup import DatabaseInitialization
from dependency_injector import containers, providers
from bot.core.services import (
    ChannelRepository,
    CommandRepository,
    GuildRepository,
    UserRepository
)


class Repositories(containers.DeclarativeContainer):
    # s_session: sessionmaker = DatabaseInitialization.init_session()
    # session: Session = s_session()

    channel_repository: ChannelRepository = providers.Singleton(ChannelRepository.ChannelRepository)
    # command_service: CommandService = providers.Singleton(CommandService.CommandService, session)
    # guild_service: GuildService = providers.Singleton(GuildService.GuildService, session)
    # user_service: UserService = providers.Singleton(UserService.UserService, session)
    # add permission service
