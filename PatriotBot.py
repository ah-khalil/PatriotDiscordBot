import logging
import inspect
import pprint
import time
import json
import sys
import os

from errors.InitializationError import InitializationError
from functools import wraps
from PatriotTask import PatriotTask
from discord.ext import commands


class PatriotBot(commands.Bot):
    UNEXPECTED_ERR = "AN ERROR OCCURRED: Please refrain from using this command until this bug is fixed"

    def __init__(self, command_prefix):
        self.task_list = {}
        self.pretty_p = pprint.PrettyPrinter()
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
        except json.decoder.JSONDecodeError as jde:
            raise InitializationError(jde)
        except AssertionError as ae:
            raise InitializationError(ae)
        except FileNotFoundError as ioe:
            raise InitializationError(ioe)
        except InitializationError as init_e:
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

        try:
            extension_list = list(self.extensions.keys())

            for task in self.task_list:
                task.stop()

            for extension in extension_list:
                self.unload_extension(f'cogs.{extension}')
        except:
            pass

    def load_extensions(self):
        try:
            self.unload_extensions()

            for filename in os.listdir('./cogs'):
                if filename.endswith('.py'):
                    self.load_extension(f'cogs.{filename[:-3]}')
        except:
            pass

    async def shutdown(self):
        try:
            for task in self.task_list:
                task.stop()
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
            pt_task.run()


patriot_bot = PatriotBot("p?")