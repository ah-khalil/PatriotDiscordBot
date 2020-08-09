from cogs import vc

DISC_ERR_DICT = {
    "ERR_NOT_CON"   : "{}, bot not connected to voice channels",
    "MSG_DISC_GO"   : "{}, disconnecting... (bye!)"
}

NAME            = "disconnect\n\n"
DESC            = "Disconnects the bot from the connected Voice Chat.\n\n"
ARGS            = "```\nUsage: \n" \
                "\tt?disconnect\n" \
                "\tt?disconnect (-h | --help)\n\n"

PERM_CHECK_LIST = [
    "connect"
]

async def disconnect(**kwargs):
    ctx = kwargs['ctx']
    common = kwargs['common']

    if common.is_voice_connected(ctx.channel.guild):
        await ctx.channel.send(DISC_ERR_DICT["MSG_DISC_GO"].format(ctx.author.mention))
        return await vc.voice_chan.disconnect()
    else:
        return await ctx.channel.send(DISC_ERR_DICT["ERR_NOT_CON"].format(ctx.author.mention))