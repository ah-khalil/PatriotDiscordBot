from dependency_injector.wiring import Provide, inject
from discord.ext import commands
from bot.core.PatriotCog import PatriotCog
from bot.core.services.ChannelRepository import ChannelRepository
from bot.core.startup.Containers import Repositories


class Genius(PatriotCog):
    def __init__(self, patriot_bot: PatriotCog, channel_repository: ChannelRepository):
        super(Genius, self).__init__(patriot_bot)

        self.patriot_bot = patriot_bot
        self.channel_repository = channel_repository
        self.messages = {
            "ERR_INV_NUM_ARGS": "{}, invalid number of arguments given",
            "ERR_NO_QUOTES": "{}, don't leave quotes empty",
            "MSG_NO_LYRICS": "{}, no lyrics found"
        }

    @commands.Cog.listener()
    async def on_ready(self):
        print("Genius cog listener - on ready")

    @commands.command()
    async def lyrics(self, *args, **kwargs):
        pass
    #  arg_msg = "```\nUsage: \n" \
    # "\tt?lyrics \"<song name>\" \"<artist name>\"\n" \
    # "\tt?lyrics (-h | --help)\n\n"
    #
    #  ctx = kwargs['ctx']
    #  common = kwargs['common']
    #
    #  args = ctx.content.split(" ", 1)
    #  regex = r"\"([^\"]*)\""
    #
    #  self.get_command_keyword(ctx.content.split(" ", 1))
    #
    #  if len(args) < 2:
    #      return await ctx.channel.send(lyrics_msg_dict["ERR_REQ_ARGS"].format(ctx.author.mention, arg_msg))
    #
    #  result = re.findall(regex, args[1])
    #
    #  if len(result) < 2 or len(result) > 2:
    #      return await ctx.channel.send(lyrics_msg_dict["ERR_INV_NUM_ARGS"].format(ctx.author.mention))
    #  else:
    #      title = result[0]
    #      artist_name = result[1]
    #
    #      if (title == "" or title == " ") or (artist_name == "" or artist_name == " "):
    #          return await ctx.channel.send(lyrics_msg_dict["ERR_NO_QUOTES"].format(ctx.author.mention))
    #
    #  search_url = common.auth["genius_auth"]["base_api_url"] + "/search?q=" + title
    #  data = {'q': title}
    #
    #  header = {
    #      "Authorization": (
    #                  common.auth["genius_auth"]["headers"]["Authorization"] + common.auth["genius_auth"]["token"])}
    #
    #  url_str = urlopen(Request(url=search_url, data=data, headers=header))
    #  url_html = url_str.read()
    #  url_str.close()
    #
    #  # response = requests.get(search_url, data=data, headers=header)
    #  json_rp = url_html.json()
    #  song_info = None
    #
    #  if "error" in json_rp:
    #      return await ctx.channel.send(common.UNEXPECTED_ERR)
    #
    #  if str(json_rp["meta"]["status"]).startswith(('4', '5')):
    #      return await ctx.channel.send("Error: " + json_rp["meta"]["message"])
    #
    #  for hit in json_rp["response"]["hits"]:
    #      if artist_name in hit["result"]["primary_artist"]["name"]:
    #          song_info = hit
    #          break
    #
    #  if song_info is not None:
    #      full_song_url = common.auth["genius_auth"]["base_song_url"] + song_info["result"]["path"]
    #      song_url_str = urlopen(Request(url=full_song_url))
    #      song_html = url_str.read()
    #      song_url_str.close()
    #      # song_page = requests.get(full_song_url)
    #      html = BeautifulSoup(song_html.text, "html.parser")
    #      [h.extract() for h in html('script')]
    #      lyrics = html.find("div", class_="lyrics").get_text()
    #      lyrics_arr = lyrics.split("\n")
    #
    #      total_length = 0
    #      lyrics_line_split = ""
    #
    #      for l in lyrics_arr:
    #          total_length += len(l)
    #          if total_length >= 1700:
    #              await ctx.channel.send(lyrics_line_split)
    #              lyrics_line_split = l
    #              total_length = len(l)
    #          else:
    #              lyrics_line_split += l + "\n"
    #
    #      return await ctx.channel.send(lyrics_line_split)
    #  else:
    #      return await ctx.channel.send(lyrics_msg_dict["MSG_NO_LYRICS"].format(ctx.author.mention))


@inject
def setup(p_bot, channel_repository: ChannelRepository = Provide[Repositories.channel_repository]):
    p_bot.add_cog(Genius(p_bot, channel_repository=channel_repository))
