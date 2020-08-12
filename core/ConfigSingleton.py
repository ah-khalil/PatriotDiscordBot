import json
import plogger

from typing import Union
from errors.CustomExceptions import (
    ConfigError,
    ConfigIOError
)

logger = plogger.get_p_logger()


class PatriotConfigMeta(type):
    _instances = {}
    _cogs_registered = []

    def __call__(cls, filename: str):
        if cls in cls._instances:
            return cls._instances[cls]
        else:
            cls._instances[cls] = super(PatriotConfigMeta, cls).__call__(filename)
            return cls._instances[cls]


class PatriotConfig(metaclass=PatriotConfigMeta):
    def __init__(self, c_filename):
        self.config_filename = c_filename
        self.config = {}

        try:
            self.update_config()
        except ConfigIOError as c_io_e:
            logger.exception(str(c_io_e))
            raise ConfigError("An error occurred when handling file: {}".format(self.config_filename))

    def get_config_cog(self, cog_name: str) -> Union[str, None]:
        if self.config is None:
            raise ConfigError("Config is not initialized")

        try:
            return self.config[cog_name]
        except KeyError as k_e:
            msg = "{} was not found in configuration".format(cog_name)
            logger.exception(str(k_e))
            raise ConfigError(msg)

    def add_cog_to_config(self, cog_name: str, val: Union[str, dict]):
        if self.config is None:
            raise ConfigError("Config is not initialized")

        if self.get_config_cog(cog_name) is not None:
            self.config[cog_name] = val

    # @todo Create a module or class that performs IO operations for clients
    # @body Currently, all file IO operations scattered across different
    # @body files, functions, and classes.
    # @body There should be a construct to centralize these calls.
    def read_config_file(self) -> str:
        try:
            f = open(self.config_filename, "r")
            return f.read()
        except IOError as io_e:
            logger.exception(str(io_e))
            raise ConfigIOError("{} was unable to be read".format(self.config_filename))
        finally:
            if not f.closed:
                try:
                    f.close()
                except IOError as ioe:
                    logger.exception(str(ioe))
                    raise ConfigIOError("{} was unable to be closed".format(self.config_filename))

    def update_config(self):
        try:
            config_str = self.read_config_file()

            if config_str is None:
                raise ValueError("Config file is empty")

            self.config = json.loads(config_str)
        except ConfigIOError as conf_io_e:
            logger.exception(str(conf_io_e))
            raise ConfigError("An error occurred updating config")
        except json.JSONDecodeError as j_e:
            logger.exception(str(j_e))
            raise ConfigIOError("Unable to load JSON object from {}".format(self.config_filename))

    def update_config_file(self):
        try:
            f = open(self.config_filename, 'w')
            f.truncate(0)
            json.dump(self.config, f)
            self.read_config_file()
        except IOError as io_e:
            logger.exception(str(io_e))
            raise ConfigIOError("{} was unable to be opened".format(self.config_filename))
        except json.JSONDecodeError as j_e:
            logger.exception(str(j_e))
            raise ConfigIOError("Unable to write object to {}".format(self.config_filename))
        except ConfigIOError as conf_io_e:
            logger.exception(str(conf_io_e))
            raise ConfigError("An error occurred updating config file")
        finally:
            if not f.closed:
                try:
                    f.close()
                except IOError as ioe:
                    logger.exception(str(ioe))
                    raise ConfigIOError("{} was unable to be closed".format(self.config_filename))
