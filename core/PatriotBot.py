import importlib.util
import logging
import pprint
import json
import sys
import os

from core.PatriotCog import PatriotCog
from core.PatriotTask import PatriotTask
from discord.ext import commands
from discord.ext.commands.errors import ExtensionNotFound
from discord.ext.commands.errors import ExtensionNotLoaded

logger = logging.getLogger("core.PatriotBot")


class PatriotBot(commands.Bot):
    def __init__(self, command_prefix):
        self.task_list = {}
        self.pretty_p = pprint.PrettyPrinter()
        self.cogs_root_dir = 'cogs.'
        self.config_file = None
        self.perms_file = None
        self.auth = None
        self.permissions = None
        self.roles = None
        self.prefix = 'p?' if command_prefix is None else command_prefix
        self.description = "A bot that does music related things"
        self.desc = "Nothing yet"
        super().__init__(command_prefix=self.prefix, description=self.description)

        try:
            logger_handler = logging.FileHandler(filename="../log.txt")
            logger_handler.setLevel(logging.DEBUG)
            logger_handler.setFormatter(logging.Formatter("\n[%(asctime)s]\n\t%(name)s - %(levelname)s - %(message)s \n"))
            logger.addHandler(logger_handler)

            self.config_file = open('../config.json', "r")
            self.perms_file = open('../permissions.json', "r+")
            self.auth = {} if os.stat('../config.json').st_size == 0 else json.load(self.config_file)
            self.read_permissions()
        except (json.decoder.JSONDecodeError, AssertionError, FileNotFoundError) as init_e:
            if logger is not None:
                logger.exception(str(init_e))

            for f_stream in [self.config_file, self.perms_file, logger]:
                try:
                    f_stream.close()
                    self.shutdown()
                except IOError as ioe:
                    if logger is not None:
                        logger.exception(str(ioe))
        finally:
            logging.shutdown()

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

        for filename in os.listdir('../cogs'):
            if filename.endswith('.py') and filename != "__init__.py" and not self.check_extension_loaded(
                    filename[:-3]):
                # self.load_extension(f'{self.cogs_root_dir + filename[:-3]}')
                self.load_extension(filename[:-3])
        # except Exception as e:
        #     print(e)

    def check_extension_loaded(self, name):
        return name in self.extensions.keys()

    def unload_extension(self, name):
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
    def load_extension(self, cog_name):
        # try:
            cog_class = None
            spec = importlib.util.find_spec(f'{self.cogs_root_dir + cog_name}')

            if spec is None:
                raise ExtensionNotFound("The following extension could not be found: {}".format(self.cogs_root_dir + cog_name))

            try:
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
            except Exception as e:
                logger.exception(str(e))
                raise ExtensionNotLoaded("The following extension could not be loaded: {}".format(self.cogs_root_dir + cog_name))

            try:
                cog_class = getattr(module, cog_name)
            except AttributeError as attr_e:
                logger.exception(str(attr_e))
                self.remove_module(module)

            # NOTE
            # If there are more than one type of cog classes, create a extension loader parent which handles the
            # loading of different types of cog classes
            try:
                if issubclass(cog_class, PatriotCog):
                    # self._load_from_module_spec(spec, cog_name)
                    sys.modules[cog_name] = module
                    setup = getattr(module, 'setup')
                    setup(self)
            except AttributeError as attr_e:
                logger.exception(str(attr_e))
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
            raise KeyError("The following module has already been removed or was never entered: {}".format(module.__name__))

        try:
            self._remove_module_references(module.__name__)
            self._call_module_finalizers(module, module.__name__)
        except Exception as e:
            logger.exception(str(e))
            raise Exception("An error occurred attempting to remove the following module: {}".format(module.__name__))

    async def shutdown(self):
        try:
            for task in self.task_list:
                self.task_list[task].stop()
                self.task_list[task] = None
        except Exception as e:
            print(e)

        return await self.logout()

    def update_permissions_file(self, whiteblack_dict):
        try:
            self.perms_file.truncate(0)
            json.dump(whiteblack_dict, self.perms_file)
            self.perms_file.seek(0)
            self.read_permissions()
        except json.decoder.JSONDecodeError as jde:
            logger.exception(str(jde))
            self.pretty_p.pprint(self.permissions)

    def read_permissions(self):
        try:
            if os.stat('../permissions.json').st_size == 0:
                self.permissions = {"user_access": {}}
            else:
                self.permissions = json.load(self.perms_file)

            self.perms_file.seek(0)
        except json.decoder.JSONDecodeError as jde:
            logger.exception(str(jde))

            if self.permissions is not None:
                self.pretty_p.pprint(self.permissions)

    def add_task(self, func, interval, **kwargs):
        target_name = kwargs.get('name', func.__name__)

        if hasattr(self.task_list, target_name):
            raise AttributeError(f"\'{target_name}\' is already registered as a task")

        pt_task = PatriotTask(name=target_name, target=func, interval=interval, **kwargs)

        if pt_task is not None:
            self.task_list[target_name] = pt_task

    def run_tasks(self):
        try:
            for target_name in self.task_list:
                self.run_task(target_name)
        except Exception as e:
            raise Exception("An error occurred trying to run all tasks" + e.__str__())

    def run_task(self, target_name):
        try:
            if target_name in self.task_list:
                if not self.task_list[target_name].is_running():
                    self.task_list[target_name].run()
        except Exception as e:
            raise Exception("An error occurred trying to run task" + target_name + e.__str__())


patriot_bot = PatriotBot("p?")