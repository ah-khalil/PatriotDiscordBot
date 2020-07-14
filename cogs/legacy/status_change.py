# from PatriotBot import *
# import re
#
# STAT_ERR_DICT = {
#     "ERR_REQ_ARGS"      : "{}, command requires the following arguments: {}",
#     "ERR_INV_ARG_NUM"   : "{}, invalid number of arguments given"
# }
#
# NAME            = "status_change\n\n"
# DESC            = "Sets the message author's status.\n\n"
# ARGS            = "```\nUsage: \n" \
#                 "\tt?status_change <\"game\">  [(offline | online | idle | dnd) [afk]]\n" \
#                 "\tt?status_change (-h | --help)\n\n"
#
# PERM_CHECK_LIST = [
#     "manage_roles"
# ]
#
# async def status_change(**kwargs):
#     async def game_maker(game_name = "Game", user_status = None, afk = False):
#         game = discord.Game(name = game_name, type = 0)
#
#         status_st = {
#             "offline"   : discord.Status.offline,
#             "online"    : discord.Status.online,
#             "idle"      : discord.Status.idle,
#             "dnd"       : discord.Status.dnd
#         }
#
#         return await common.change_presence(game = game, status = status_st.get(user_status, None), afk = afk)
#
#     ctx = kwargs['ctx']
#     common = kwargs['common']
#     args        = ctx.content.split(" ", 1)
#     regex       = r"\"([^\"]*)\""
#
#     if len(args) < 2:
#         return await ctx.channel.send(STAT_ERR_DICT["ERR_REQ_ARGS"].format(ctx.author.mention, ARGS))
#
#     args_split = re.findall(regex, args[1])
#
#     if len(args_split) < 1 or len(args_split) > 3:
#         return await ctx.channel.send(STAT_ERR_DICT["ERR_INV_ARG_NUM"].format(ctx.author.mention))
#
#     await game_maker(*args_split)
