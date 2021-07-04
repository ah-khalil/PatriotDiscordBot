import pprint
import re

CHPM_ERR_DICT = {'ERR_REQ_ARGS': "{}, command requires the following arguments: {}",
                 'ERR_INV_USR': "{}, you must be the server owner",
                 'ERR_INV_COM': "{}, command was not found",
                 'ERR_INV_ROL': "{}, role was not found on server",
                 'ERR_INV_CTX': "{}, make sure role, bot command exist and that the user/role does or doesn't already "
                                "exist in the corresponding list"}

NAME = "change_perm\n\n"
DESC = "Change the permissions set for any bot command.\n\n"
ARGS = "```\nUsage: \n" \
       "\tt?change_perm (whitelist_user | blacklist_user) <bot-command> (-r | -a) @<user>\n" \
       "\tt?change_perm (-h | --help)\n\n" \
       "Options: \n" \
       "\t -r, \t\t\t\t remove user\n" \
       "\t -a, \t\t\t\t add user\n```"

PERM_CHECK_LIST = [
    "manage_roles",
    "manage_guild",
    "manage_channels"
]


async def change_perm(**kwargs):
    ctx = kwargs['ctx']
    common = kwargs['common']
    checks = kwargs['checks']

    args = ctx.content.split(" ", 1)
    set_wbru_regex = r'(whitelist_user|blacklist_user) (\S+) (-[ra]) (<@\S+>)'

    author = ctx.author
    owner = ctx.author.guild.owner
    server_id = ctx.author.guild.id

    if len(args) < 2:
        return await ctx.channel.send(CHPM_ERR_DICT["ERR_REQ_ARGS"].format(ctx.author.mention, ARGS))

    rgx_match = re.findall(set_wbru_regex, args[1])

    pprint.pprint(rgx_match)

    if len(rgx_match) <= 0 and len(rgx_match[0]) < 4:
        return await ctx.channel.send(CHPM_ERR_DICT["ERR_REQ_ARGS"].format(ctx.author.mention, ARGS))

    op, bot_command, op_mod, subject = rgx_match[0][0], rgx_match[0][1], rgx_match[0][2], rgx_match[0][3]
    dict_idx = args[1].split(" ")[0] + "s"

    if not checks.check_command(bot_command, server_id):
        return await ctx.channel.send(CHPM_ERR_DICT["ERR_INV_COM"].format(ctx.author.mention))

    {
        "-a": checks.add_user_to_list,
        "-r": checks.remove_user_from_list
    }[op_mod](server_id, subject, bot_command, dict_idx)
