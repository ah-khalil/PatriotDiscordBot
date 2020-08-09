from core.PatriotBot import patriot_bot
import pprint


@patriot_bot.event
async def on_ready():
    print(f"Logged in as {patriot_bot.user.name}")
    print("=========================================================")


@patriot_bot.command
async def test_command():
    print("I'm a shit programmer")

if __name__ == "__main__":
    pp = pprint.PrettyPrinter()
    patriot_bot.load_extensions()
    patriot_bot.run_tasks()
    patriot_bot.run(patriot_bot.auth["discord_client_auth"]["token"])

# module_dict = {}
# checker = checks.Checks(module_dict)

# @patriot_bot.check_time
# def recurse_get_modules(path_name, super_set):
#     super_set[path_name] = []
#     for importer, name, ispkg in pkgutil.iter_modules([path_name]):
#         if ispkg:
#             recurse_get_modules(path_name + '/' + name, super_set)
#         else:
#             mod_obj = importer.find_module(name).load_module(name)
#             module_dict[name] = {
#                 "module": mod_obj,
#                 "command": getattr(mod_obj, name),
#                 "perm_check": getattr(mod_obj, "PERM_CHECK_LIST"),
#                 "description": getattr(mod_obj, "DESC"),
#                 "arguments": getattr(mod_obj, "ARGS"),
#                 "timeout_list": {}
#             }
#
#             super_set[path_name].append(name)


# @patriot_bot.event
# async def on_message(ctx):
#     if ctx.author.id != patriot_bot.user.id and ctx.content.startswith(patriot_bot.prefix):
#         com_split = []
#         command_name = ""
#
#         try:
#             now = time.time()
#             user_id = ctx.author.mention
#             server_id = ctx.author.guild.id
#             msg_split = ctx.content.split(" ")
#             cmd_split = msg_split[0].split("?")
#
#             if len(cmd_split) != 2:
#                 raise CommandNotFoundError()
#
#             command_name = cmd_split[1]
#
#             print(command_name)
#
#             # if command_name not in module_dict:
#             #     raise CommandNotFoundError()
#             #
#             # # retrieve the function callback from the dictionary using the name of the command
#             # func_callback = module_dict[command_name]["command"]
#             # func_perm_chk = module_dict[command_name]["perm_check"]
#             #
#             # # check if the user has the permissions needed to use the command
#             # if not checker.check_permissions(ctx.author.guild_permissions, func_perm_chk):
#             #     if not checker.is_whitelisted(server_id, user_id, command_name):
#             #         err_msg = f"{ctx.author.mention}, you require the following permissions enabled: \n"
#             #
#             #         for perm_str in module_dict[command_name]["perm_check"]:
#             #             err_msg += perm_str_propefier(perm_str) + "\n"
#             #
#             #         return await ctx.channel.send(err_msg)
#             # else:
#             #     if checker.is_blacklisted(server_id, user_id, command_name):
#             #         err_msg = f"{ctx.author.mention}, you have been blacklisted from using this command: {command_name} \n"
#             #         return await ctx.channel.send(err_msg)
#             #
#             # # check to see if the user is in the timeout list for the command
#             # if ctx.author.id not in module_dict[command_name]["timeout_list"]:
#             #     module_dict[command_name]["timeout_list"][ctx.author.id] = ""
#             #
#             # # check to see if the user is within the timeout range of the command
#             # # if so, tell the user to wait; if not, run the command
#             # if module_dict[command_name]["timeout_list"][ctx.author.id] == "" or module_dict[command_name]["timeout_list"][ctx.author.id] + 5.0 < now:
#             #     module_dict[command_name]["timeout_list"][ctx.author.id] = now
#             #     del msg_split[0]
#             #     await func_callback(ctx=ctx, common=PATRIOTBOT, checks=checker)
#             # else:
#             #     await ctx.channel.send(f"{ctx.author.mention}, you need to wait for at least five seconds before using that command again")
#
#         except CommandNotFoundError:
#             await ctx.channel.send(f"{ctx.author.mention}, The following command was not found: {command_name}")
#         # except BaseException as e:
#         #     print(e)
#         #     await ctx.channel.send("Something went wrong, please try again later")




