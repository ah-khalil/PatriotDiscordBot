from cogs import vc

CON_ERR_DICT = {
    "ERR_IS_CON"    : "{}, I'm already connected to a voice channel",
    "ERR_USR_NCON"  : "{}, you should be connected to a voice channel"
}

NAME            = "connect\n\n"
DESC            = "Connects bot to the specified Voice Chat or that of the message author's.\n\n"
ARGS            = "```\nUsage: \n" \
                "\tt?connect\n" \
                "\tt?connect (-h | --help)\n\n"

PERM_CHECK_LIST = [
    "connect",
    "speak",
    "mute_members",
    "deafen_members"
]

#connects the bot to the voice channel
async def connect(**kwargs):
    ctx = kwargs['ctx']
    common = kwargs['common']

    if common.is_voice_connected(ctx.guild):
        return await ctx.channel.send(CON_ERR_DICT["ERR_IS_CON"].format(ctx.author.mention))
    if ctx.author.voice_channel is None:
        return await ctx.channel.send(CON_ERR_DICT["ERR_USR_NCON"].format(ctx.author.mention))

    vc.voice_chan = await common.join_voice_channel(ctx.author.voice_channel)
    vc.voice_chan = ctx.author.voice_channel
    print(vc.voice_chan)

def ytp():
    pass