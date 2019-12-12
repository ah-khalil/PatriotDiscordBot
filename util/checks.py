from PatriotBot import patriot_bot

import discord
import pprint

class Checks:
    def __init__(self, module_dict):
        self.com_obj = patriot_bot
        self.module_dict = module_dict
        self.whiteblack_dict = patriot_bot.permissions

    def check_permissions(self, permission, to_check_list):
        bool_check = 0
        to_check_map = {
            "create_instant_invite" : permission.create_instant_invite,
            "kick_members"          : permission.kick_members,
            "ban_members"           : permission.ban_members,
            "manage_channels"       : permission.manage_channels,
            "manage_guild"          : permission.manage_guild,
            "add_reactions"         : permission.add_reactions,
            "view_audit_logs"       : permission.view_audit_log,
            "read_messages"         : permission.read_messages,
            "send_messages"         : permission.send_messages,
            "send_tts_messages"     : permission.send_tts_messages,
            "manage_messages"       : permission.manage_messages,
            "embed_links"           : permission.embed_links,
            "attach_files"          : permission.attach_files,
            "read_message_history"  : permission.read_message_history,
            "mention_everyone"      : permission.mention_everyone,
            "external_emojis"       : permission.external_emojis,
            "connect"               : permission.connect,
            "speak"                 : permission.speak,
            "mute_members"          : permission.mute_members,
            "deafen_members"        : permission.deafen_members,
            "move_members"          : permission.move_members,
            "use_voice_activation"  : permission.use_voice_activation,
            "change_nickname"       : permission.change_nickname,
            "manage_nicknames"      : permission.manage_nicknames,
            "manage_roles"          : permission.manage_roles,
            "manage_webhooks"       : permission.manage_webhooks,
            "manage_emojis"         : permission.manage_emojis
        }

        for check in to_check_list:
            bool_check += to_check_map[check]

        return bool_check == len(to_check_list)

    def check_server(self, server_id):
        if server_id not in self.whiteblack_dict["user_access"]:
            self.whiteblack_dict["user_access"][server_id] = {
                command: {
                    "whitelist_users": [],
                    "blacklist_users": []
                } for command in self.module_dict
            }

            self.com_obj.update_permissions_file(self.whiteblack_dict)

    def is_blacklisted(self, server_id, user_id, command_name):
        self.check_server(server_id)

        return user_id in self.whiteblack_dict["user_access"][server_id][command_name]["blacklist_users"]

    def is_whitelisted(self, server_id, user_id, command_name):
        self.check_server(server_id)

        return user_id in self.whiteblack_dict["user_access"][server_id][command_name]["whitelist_users"]

    def check_command(self, bot_command, server_id):
        return bot_command in self.whiteblack_dict["user_access"][server_id]

    def add_user_to_list(self, server_id, user_id, command_name, list_idx):
        {
            "blacklist_users" : self.add_user_to_blacklist,
            "whitelist_users" : self.add_user_to_whitelist
        }[list_idx](server_id, user_id, command_name)

        self.com_obj.update_permissions_file(self.whiteblack_dict)

    def remove_user_from_list(self, server_id, user_id, command_name, list_idx):
        {
            "blacklist_users" : self.remove_user_from_blacklist,
            "whitelist_users" : self.remove_user_from_whitelist
        }[list_idx](server_id, user_id, command_name)

        self.com_obj.update_permissions_file(self.whiteblack_dict)

    def add_user_to_blacklist(self, server_id, user_id, command_name):
        if self.is_blacklisted(server_id, user_id, command_name):
            return

        self.remove_user_from_whitelist(server_id, user_id, command_name)
        self.whiteblack_dict["user_access"][server_id][command_name]["blacklist_users"].append(user_id)

    def add_user_to_whitelist(self, server_id, user_id, command_name):
        if self.is_whitelisted(server_id, user_id, command_name):
            return

        self.remove_user_from_blacklist(server_id, user_id, command_name)
        self.whiteblack_dict["user_access"][server_id][command_name]["whitelist_users"].append(user_id)

    def remove_user_from_blacklist(self, server_id, user_id, command_name):
        if self.is_blacklisted(server_id, user_id, command_name):
            self.whiteblack_dict["user_access"][server_id][command_name]["blacklist_users"].remove(user_id)

    def remove_user_from_whitelist(self, server_id, user_id, command_name):
        if self.is_whitelisted(server_id, user_id, command_name):

            self.whiteblack_dict["user_access"][server_id][command_name]["whitelist_users"].remove(user_id)

    def print_dict(self):
        pprint.pprint(self.whiteblack_dict)