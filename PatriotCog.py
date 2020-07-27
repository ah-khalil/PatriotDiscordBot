import re
from typing import Union
from discord.ext.commands.cog import Cog
from errors.CustomExceptions import CommandProcessingError


class PatriotCog(Cog):
    def __init__(self):
        super(PatriotCog, self).__init__()
        self.__unloadable = True
        self.__messages = {
            "ERR_REQ_ARGS": "{}, command requires the following arguments: {}",
            "UNEXPECTED_ERROR": "{}, unfortunately an error occurred",
            "COMMAND_NOT_FOUND": "the following command was not found: {}"
        }

    @property
    def unloadable(self) -> bool:
        return self.__unloadable

    @property
    def messages(self) -> dict:
        return dict(self.__messages)

    @messages.setter
    def messages(self, messages: dict):
        self.__messages = messages

    @staticmethod
    def get_command_keyword(command, regex):
        try:
            keyword_arr = []
            matches = re.finditer(regex, command, re.MULTILINE)

            for match_num, match in enumerate(matches, start=1):
                if len(match.groups()) == 0:
                    keyword_arr.append(match.group())
                else:
                    for group_num in range(0, len(match.groups())):
                        group_num = group_num + 1
                        keyword_arr.append(match.group(group_num))

            return keyword_arr
        except re.error as re_err:
            raise CommandProcessingError("Supplied regex is not valid")
        except Exception as e:
            raise BaseException("An error occurred")
