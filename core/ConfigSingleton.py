from typing import Union
import json
import plogger

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
        self.config_str = self.read_config_file()

        if self.config_str is None:
            return

        self.config = json.loads(self.config_str)

    def get_config_cog(self, cog_name: str) -> Union[str, None]:
        if self.config is None:
            logger.error("Config is not initialized")
            return

        try:
            return self.config[cog_name]
        except KeyError as k_e:
            logger.exception(str(k_e))
            logger.error("{} was not found in configuration".format(cog_name))

    def add_cog_to_config(self, cog_name: str, val: Union[str, dict]):
        if self.config is None:
            logger.error("Config is not initialized")
            return

        if self.get_config_cog(cog_name) is not None:
            self.config[cog_name] = val

    # @todo Create a module or class that performs IO operations for clients
    # @body Currently, all file IO operations scattered across different
    # @body files, functions, and classes.
    # @body There should be a construct to centralize these calls.
    def read_config_file(self) -> str:
        if self.config_str is not None:
            logger.info("Logger has already read file")

        try:
            f = open(self.config_filename, "r")
            f_str = f.read()

            return f_str
        except IOError as io_e:
            logger.exception(str(io_e))
            logger.error("{} was unable to be read".format(self.config_filename))
        finally:
            try:
                f.close()
            except IOError as ioe:
                logger.exception(str(ioe))
                logger.error("{} was unable to be closed".format(self.config_filename))

    def update_config_file(self):
        if self.config is None:
            logger.error("Config is not initialized")

        try:
            f = open(self.config_filename, 'w')
            f.truncate(0)
            json.dump(self.config, self.config_filename)
            self.read_config_file()
        except IOError as io_e:
            logger.exception(str(io_e))
            logger.error("{} was unable to be opened".format(self.config_filename))
        except json.JSONDecodeError as j_e:
            logger.exception(str(j_e))
            logger.error("Unable to write object to {}".format(self.config_filename))
        finally:
            try:
                f.close()
            except IOError as ioe:
                logger.exception(str(ioe))
                logger.error("{} was unable to be closed".format(self.config_filename))
