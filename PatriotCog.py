from discord.ext import commands
from discord.ext.commands.cog import Cog
from PatriotTask import PatriotTask


class PatriotCog(Cog):
    def __init__(self):
        self.__unloadable = True
        super(PatriotCog, self).__init__()

    @property
    def unloadable(self):
        return self.__unloadable

    @unloadable.setter
    def unloadable(self, value):
        if not isinstance(value, (int, float)):
            return

        self.__unloadable = value
