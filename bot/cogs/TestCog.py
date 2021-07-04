from typing import Callable

from discord.abc import GuildChannel
from discord.ext import commands
from discord.ext.commands import Context
from dependency_injector.wiring import Provider, inject
from bot.core.models.Channel import Channel
from bot.core.services.ChannelRepository import ChannelRepository
from bot.core.startup.Containers import Repositories
from bot.core.PatriotBot import PatriotBot
from bot.core.PatriotCog import PatriotCog


class TestCog(PatriotCog):
    def __init__(self, patriot_bot: PatriotBot, channel_repo: ChannelRepository):
        super(TestCog, self).__init__(patriot_bot)
        self.channel_repo = channel_repo

    @commands.Cog.listener()
    async def on_ready(self):
        print("TestCog cog listener - on ready")

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, guild_channel: GuildChannel):
        self.channel_repo.delete()

    @commands.command()
    async def add_channel(self, ctx: Context, name: str, channel_type: str, is_nsfw: str):
        if channel_type.lower not in ['text', 'voice']:
            # some sort of error back to the author
            pass

        channel_name = name
        channel_type = channel_type if channel_type in ['text', 'voice'] else ""
        channel_is_nsfw = is_nsfw is not None and is_nsfw.lower() in ['true', '1', 't', 'y', 'yes', 'yeah', 'yup',
                                                                      'certainly', 'uh-huh']

        self.channel_repo.add(100, name=channel_name, type=channel_type, is_nsfw=channel_is_nsfw)

@inject
def setup(p_bot: PatriotBot,
          channel_repo_provider: Callable[..., ChannelRepository] = Provider[Repositories.channel_repository]):
    p_bot.add_cog(TestCog(p_bot, channel_repo_provider()))
