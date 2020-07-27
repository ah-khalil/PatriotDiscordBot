import importlib
import logging
import inspect
import pprint
import time
import json
import sys
import os

from functools import wraps
from PatriotCog import PatriotCog
from PatriotTask import PatriotTask
from discord.ext import commands
from discord.ext.commands.errors import ExtensionNotFound
from discord.ext.commands.errors import ExtensionNotLoaded


class PatriotBot(commands.Bot):
    UNEXPECTED_ERR = "AN ERROR OCCURRED: Please refrain from using this command until this bug is fixed"

    def __init__(self, command_prefix):
        self.task_list = {}
        self.pretty_p = pprint.PrettyPrinter()
        self.cogs_root_dir = 'cogs.'
        self.config_file = None
        self.perms_file = None
        self.auth = None
        self.logger = None
        self.permissions = None
        self.roles = None
        self.prefix = 'p?' if command_prefix is None else command_prefix
        self.description = "A bot that does music related things"
        self.desc = "Nothing yet"
        super().__init__(command_prefix=self.prefix, description=self.description)

        try:
            self.config_file = open('config.json', "r")
            self.perms_file = open('permissions.json', "r+")
            self.auth = {} if os.stat('config.json').st_size == 0 else json.load(self.config_file)
            self.read_permissions()
            self.logger = logging.getLogger('log.txt')
        except (json.decoder.JSONDecodeError, AssertionError, FileNotFoundError) as init_e:
            if self.logger is None:
                pass
            else:
                self.logger.exception(init_e.get_message())

            for f_stream in [self.config_file, self.perms_file, self.logger]:
                try:
                    f_stream.close()
                    self.shutdown()
                except IOError as ioe:
                    pass
        finally:
            pass

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

        for filename in os.listdir('./cogs'):
            if filename.endswith('.py') and filename != "__init__.py" and not self.check_extension_loaded(filename[:-3]):
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

    def load_extension(self, cog_name):
        # try:
            module = importlib.import_module(f'{self.cogs_root_dir + cog_name}')
            cog_class = getattr(module, cog_name)

            # NOTE
            # If there are more than one type of cog classes, create a extension loader parent which handles the
            # loading of different types of cog classes

            if issubclass(cog_class, PatriotCog):
                self._load_from_module_spec(module, cog_name)
        # except ImportError as e:
        #     raise ExtensionNotFound(cog_name, e) from e
        # except Exception as e:
        #     raise Exception("PatriotCog type check error occurred")

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
            self.logger.exception(jde)
            self.pretty_p.pprint(self.permissions)

    def read_permissions(self):
        try:
            self.permissions = {"user_access": {}} if os.stat('permissions.json').st_size == 0 else json.load(self.perms_file)
            self.perms_file.seek(0)
        except json.decoder.JSONDecodeError as jde:
            self.logger.exception(jde)

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