# from cogs.billboard import song_list
# from cogs.billboard.util import common as bb_common
# from cogs.billboard.models.SongInfo import SongInfo
# import discord
#
# NAME = "hot100\n\n"
# DESC = "Returns a sublist of the current day's BillBoard's Hot 100, filtered based on the query.\n\n"
# ARGS = "\nUsage: \n" \
#        "\tt?hot100 \"[rank|name|artist|features|last_week|peak_pos|weeks_on_chart]: (SEARCH TERM)\"\n" \
#        "\tt?hot100 (-h | --help)\n\n"
#
# PERM_CHECK_LIST = [
#     "send_messages"
# ]
#
#
# async def hot100(**kwargs):
#     hot100_msg_dict = {"MSG_NOT_RES": "song not found"}
#
#     ctx = kwargs['ctx']
#     res_arr = []
#
#     query_obj = await bb_common.input_verifier(ctx=ctx, bill_item=SongInfo)
#     operation = (lambda a, b: a in b)
#
#     try:
#         query_obj["query_item"] = int(query_obj["query_item"].strip())
#         operation = (lambda a, b: a == int(b))
#     except ValueError:
#         pass  # it is a string, forget about it
#     except Exception as e:
#         raise Exception(e)
#
#     print("Category: " + str(query_obj["query_category"]))
#     print("Item: " + str(query_obj["query_item"]))
#
#     for song in song_list:
#         try:
#             if operation(query_obj["query_item"], song.__getattribute__(query_obj["query_category"])):
#                 song_embed = discord.Embed(
#                     title=song.name,
#                     type='rich',
#                     color=discord.Color.blue()
#                 )
#
#                 song_embed.set_footer(text="Provided By Billboard")
#                 song_embed.set_thumbnail(url=song.get_thumbnail_url())
#                 song_embed.add_field(name="Artist", value=song.artist, inline=True)
#                 song_embed.add_field(name="Rank", value=song.rank, inline=True)
#                 song_embed.add_field(name="Featuring", value=song.features_string(), inline=True)
#                 song_embed.add_field(name="Last Week's Position", value=song.last_week, inline=True)
#                 song_embed.add_field(name="Peak Position", value=song.peak_pos, inline=True)
#                 song_embed.add_field(name="Weeks on Chart", value=song.weeks_on_chart, inline=True)
#
#                 res_arr.append(song_embed)
#
#                 if len(res_arr) > 0:
#                     return [await ctx.channel.send(embed=song_embed) for song_embed in res_arr]
#
#                 return await ctx.channel.send(hot100_msg_dict["MSG_NOT_RES"].format(ctx.author.mention))
#         except ValueError:
#             pass
