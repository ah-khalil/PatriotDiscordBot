import os

from bot.core.errors.CustomExceptions import ConfigurationError


class CoreConfig:
    @staticmethod
    def get_connection_string():
        try:
            return os.environ.get("ConnectionString")
        except KeyError:
            ConfigurationError("could not find environmental variable, ConnectionString")

    @staticmethod
    def get_client_id():
        try:
            return os.environ.get("DiscordClientId")
        except KeyError:
            ConfigurationError("could not find environmental variable, DiscordClientId")

    @staticmethod
    def get_client_secret():
        try:
            return os.environ.get("DiscordClientSecret")
        except KeyError:
            ConfigurationError("could not find environmental variable, DiscordClientSecret")

    @staticmethod
    def get_token():
        try:
            return os.environ.get("DiscordToken")
        except KeyError:
            ConfigurationError("could not find environmental variable, DiscordToken")

    @staticmethod
    def get_bot_root():
        try:
            return os.environ.get("BotRoot")
        except KeyError:
            ConfigurationError("could not find environmental variable, BotRoot")

    @staticmethod
    def get_cog_root():
        try:
            return os.environ.get("CogRoot")
        except KeyError:
            ConfigurationError("could not find environmental variable, CogRoot")


class GeniusConfig:
    @staticmethod
    def get_client_id():
        try:
            return os.environ.get("GeniusClientId")
        except KeyError:
            ConfigurationError("could not find environmental variable, GeniusClientId")

    @staticmethod
    def get_client_secret():
        try:
            return os.environ.get("GeniusClientSecret")
        except KeyError:
            ConfigurationError("could not find environmental variable, GeniusClientSecret")

    @staticmethod
    def get_token():
        try:
            return os.environ.get("GeniusToken")
        except KeyError:
            ConfigurationError("could not find environmental variable, GeniusToken")
