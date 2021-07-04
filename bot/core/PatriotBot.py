import importlib.util
import logging
import sys
import os

from typing import Optional
from pathlib import Path
from bot.core.config.Config import CoreConfig
from discord.ext import commands
from bot.core.PatriotCog import PatriotCog
from discord.ext.commands.errors import ExtensionNotFound
from discord.ext.commands.errors import ExtensionNotLoaded
from bot.core.startup.Containers import Repositories
from bot.core.errors.CustomExceptions import (
    InitializationError,
    ConfigurationError
)

logger = logging.getLogger("bot.core.PatriotBot")


class PatriotBot(commands.Bot):
    def __init__(self, command_prefix: str, description: Optional[str] = "No description"):
        self.task_list = {}
        self.prefix = 'p?' if command_prefix is None else command_prefix
        self.description = description
        self.cogs_root_dir = CoreConfig.get_cog_root()
        self.service_containers: Repositories = Repositories()

        super().__init__(command_prefix=self.prefix, description=self.description)

        try:
            logger_handler = logging.FileHandler(filename="log.txt")
            logger_handler.setLevel(logging.DEBUG)
            logger_handler.setFormatter(
                logging.Formatter("\n[%(asctime)s]\n\t%(name)s - %(levelname)s - %(message)s \n\n"))
            logger.addHandler(logger_handler)
        except Exception as e:
            if logger is not None:
                logger.exception(e.__str__())
                logging.shutdown()

    async def shutdown(self):
        try:
            for task in self.task_list:
                self.task_list[task].stop()
                self.task_list[task] = None
        except Exception as e:
            print(e)

        return await self.logout()

    def unload_extensions(self):
        if self.extensions.__len__() == 0:
            return

        # try:
        extension_list = list(self.extensions.keys())
        print(extension_list)

        for task in self.task_list:
            self.task_list[task].stop()
            self.task_list[task] = None

        for extension in extension_list:
            self.unload_extension(extension)

        print(extension_list)
        # except:
        #     pass

    def load_extensions(self):
        # try:
        # should skip if the only extensions loaded are not unloadable (cant unload)
        self.unload_extensions()

        if self.cogs_root_dir is None:
            raise InitializationError("root extension directory was not found")

        cog_path = Path(self.cogs_root_dir)

        try:
            for file_path in cog_path.iterdir():
                filename = file_path.name

                if filename.endswith('.py') and filename != "__init__.py" and not self.check_extension_loaded(
                        filename[:-3]):
                    # self.load_extension(f'{self.cogs_root_dir + filename[:-3]}')
                    self.load_extension(filename[:-3])
        except FileNotFoundError as fnf_e:
            logger.exception(fnf_e.__str__())
            raise InitializationError("root extension directory was not found")
        # except Exception as e:
        #     logger.exception(e.__str__())
        #     raise InitializationError("an error occurred while loading extensions")

        if self.extensions.__len__() == 0:
            logger.warning("No extensions were loaded")

    def check_extension_loaded(self, name):
        return name in self.extensions.keys()

    def unload_extension(self, name: str, *, package=None):
        # try:
        if not self.check_extension_loaded(name):
            raise ExtensionNotLoaded(name)

        cog = self.extensions.get(name)
        cog_class_obj = self.get_extension_class(name)

        if cog_class_obj.unloadable:
            self._remove_module_references(cog.__name__)
            self._call_module_finalizers(cog, name)

    # except Exception as e:
    #     pass

    def get_extension_class(self, name):
        # try:
        cog = self.extensions.get(name)
        cog_class = getattr(cog, name)
        return cog_class(self)

    # except Exception as e:
    #     pass

    # @todo Handle duplicate code for module loading
    # @body load_extension() function contains code that loads a module from a spec
    # @body to obtain a class definition for a potential cog.
    # @body The class definition is needed as it determines if the cog is a subclass
    # @body of PatriotCog, thus determining whether or not it should loaded.
    # @body The spec and module loading components are also found in _load_from_module_spec()
    # @body in bot.py, presenting duplicate code.
    def load_extension(self, cog_name: str, *, package=None):
        # try:
        module = None
        cog_class = None
        spec = importlib.util.spec_from_file_location(cog_name, self.cogs_root_dir + "\\" + cog_name + ".py")

        print(cog_name)

        if spec is None:
            raise ExtensionNotFound(
                "The following extension could not be found: {}".format(self.cogs_root_dir + cog_name))

        try:
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            self.service_containers.wire(modules=[module])
            cog_class = getattr(module, cog_name)
        except AttributeError as attr_e:
            logger.exception(str(attr_e))

            print(attr_e.__str__())

            if module is not None:
                self.remove_module(module)
        except Exception as e:
            logger.exception(str(e))
            raise ExtensionNotLoaded("The following extension could not be loaded: {}".format(cog_name))
        # NOTE
        # If there are more than one type of cog classes, create a extension loader parent which handles the
        # loading of different types of cog classes
        try:
            if issubclass(cog_class, PatriotCog):
                # self._load_from_module_spec(spec, cog_name)
                print("Cog Class Name: {}".format(cog_class))
                print("Cog Name: {}\n".format(cog_name))
                sys.modules[cog_name] = module
                setup = getattr(module, 'setup')
                setup(self)
        except AttributeError as attr_e:
            logger.exception(str(attr_e))

            print(attr_e.__str__())

            self.remove_module(module)

    # except ImportError as e:
    #     raise ExtensionNotFound(cog_name, e) from e
    # except Exception as e:
    #     raise Exception("PatriotCog type check error occurred")

    def remove_module(self, module):
        try:
            if module.__name__ in sys.modules:
                del sys.modules[module.__name__]
        except KeyError as key_e:
            logger.exception(str(key_e))
            raise KeyError(
                "The following module has already been removed or was never entered: {}".format(module.__name__))

        try:
            self._remove_module_references(module.__name__)
            self._call_module_finalizers(module, module.__name__)
        except Exception as e:
            logger.exception(str(e))
            raise Exception("An error occurred attempting to remove the following module: {}".format(module.__name__))

    # def invoke(self, ctx):
    #     if checks.has_user_access(ctx) and checks.has_channel_access(ctx):
    #         super(PatriotBot, self).invoke(ctx)


patriot_bot = PatriotBot("p?")
