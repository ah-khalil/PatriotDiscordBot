from core.PatriotCog import PatriotCog
from discord.ext import commands


class ExtensionControl(PatriotCog):
    def __init__(self, patriot_bot):
        super(ExtensionControl, self).__init__()

        self.patriot_bot = patriot_bot
        self.unloadable = False

    @commands.Cog.listener()
    async def on_ready(self):
        print("ExtensionController is ready")

    @commands.command()
    async def ue(self, ctx):
        self.patriot_bot.unload_extensions()

    @commands.command()
    async def le(self, ctx):
        self.patriot_bot.load_extensions()


def setup(p_bot):
    p_bot.add_cog(ExtensionControl(p_bot))
