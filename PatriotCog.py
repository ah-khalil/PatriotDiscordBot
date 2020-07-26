import re
from typing import Union
from discord.ext.commands.cog import Cog

# @todo Create a dictionary listing information about subclass commands
# @body Subclasses of PatriotCog contain commands that have information specific
# @body to them (e.g. regexes, help messages, etc.). They all need to be contained
# @body within a dictionary that are first-order keyed with command names which each point
# @body to another dictionary with an information title - information value pairing
class PatriotCog(Cog):
    def __init__(self):
        super(PatriotCog, self).__init__()
        self.__unloadable = True
        self.__command_messages = None
        self.__command_references = None
        self.__messages = {
            "ERR_REQ_ARGS": "{}, command requires the following arguments: {}",
            "UNEXPECTED_ERROR": "{}, unfortunately an error occurred"
        }

    @property
    def unloadable(self) -> bool:
        return self.__unloadable

    @property
    def messages(self) -> dict:
        return dict(self.__messages)

    @messages.setter
    def messages(self, messages : dict):
        self.__messages = messages

    def get_command_keyword(self, command):
        pass
        # if self.command_regex is None:
        #     raise TypeError("command regex is None")
        #
        # try:
        #     keyword_arr = []
        #     matches = re.finditer(self.command_regex, command, re.MULTILINE)
        #
        #     for match_num, match in enumerate(matches, start=1):
        #         if len(match.groups()) == 0:
        #             keyword_arr.append(match.group())
        #         else:
        #             for group_num in range(0, len(match.groups())):
        #                 group_num = group_num + 1
        #                 keyword_arr.append(match.group(group_num))
        #
        #     return keyword_arr
        # except Exception as e:
        #     raise BaseException("An error occurred")
