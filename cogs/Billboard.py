import re
import threading

from PatriotCog import PatriotCog
from bs4 import BeautifulSoup as soup
from discord import Embed, Color
from discord.ext import commands
from discord.ext.commands import Cog
from urllib.request import (Request, urlopen)
from cogs.billboard import (
    hot_url,
    bill200_url,
    hdr
)

from entities.SongInfo import SongInfo
from entities.AlbumInfo import AlbumInfo
from entities.BillboardItem import BillboardItem


class Billboard(PatriotCog):
    def __init__(self, patriot_bot):
        super(Billboard, self).__init__()

        self.song_list = []
        self.album_list = []
        self.lock = threading.Lock()
        self.patriot_bot = patriot_bot
        self.patriot_bot.add_task(self.update_billboard_items, 60 * 60 * 24)


    @commands.Cog.listener()
    async def on_ready(self):
        print("We in this bitch")

    @commands.command()
    async def hot100(self, ctx):
        hot100_msg_dict = {"MSG_NOT_RES": "song not found"}

        res_arr = []

        query_obj = await self.input_verifier(ctx=ctx, bill_item=SongInfo)
        operation = (lambda a, b: a in b)

        try:
            query_obj["query_item"] = int(query_obj["query_item"].strip())
            operation = (lambda a, b: a == int(b))
        except ValueError:
            pass  # it is a string, forget about it
        except Exception as e:
            raise Exception(e)

        print("Category: " + str(query_obj["query_category"]))
        print("Item: " + str(query_obj["query_item"]))

        for song in self.song_list:
            try:
                if operation(query_obj["query_item"], song.__getattribute__(query_obj["query_category"])):
                    song_embed = Embed(
                        title=song.name,
                        type='rich',
                        color=Color.blue()
                    )

                    song_embed.set_footer(text="Provided By Billboard")
                    song_embed.set_thumbnail(url=song.get_thumbnail_url())
                    song_embed.add_field(name="Artist", value=song.artist, inline=True)
                    song_embed.add_field(name="Rank", value=song.rank, inline=True)
                    song_embed.add_field(name="Featuring", value=song.features_string(), inline=True)
                    song_embed.add_field(name="Last Week's Position", value=song.last_week, inline=True)
                    song_embed.add_field(name="Peak Position", value=song.peak_pos, inline=True)
                    song_embed.add_field(name="Weeks on Chart", value=song.weeks_on_chart, inline=True)

                    res_arr.append(song_embed)

                    if len(res_arr) > 0:
                        return [await ctx.channel.send(embed=song_embed) for song_embed in res_arr]

                    return await ctx.channel.send(hot100_msg_dict["MSG_NOT_RES"].format(ctx.author.mention))
            except ValueError:
                pass

    @staticmethod
    async def input_verifier(**kwargs):
        bill_comm_err_dict = {
            "ERR_REQ_ARGS": "{}, command requires the following arguments: {}",
            "ERR_QUERY": "{}, please provide one query",
            "ERR_QUERY_TERM": "{}, please provide one query term",
            "ERR_INV_CAT": "{}, invalid song property"
        }

        ctx = kwargs['ctx']

        try:
            bill_item = kwargs['bill_item']
            args = ctx.content.split(" ", 1)
            regex = r"\"([^\"]*)\""

            if len(args) < 2:
                return await ctx.channel.send(bill_comm_err_dict["ERR_REQ_ARGS"].format(ctx.author.mention))

            query = re.findall(regex, args[1])

            if len(query) != 1:
                return await ctx.channel.send(bill_comm_err_dict["ERR_NO_QUERY"].format(ctx.author.mention))

            query_cln_spl = query[0].split(":")

            if len(query_cln_spl) != 2 or (len(query_cln_spl) > 2 and query_cln_spl[1].strip() == ""):
                return await ctx.channel.send(bill_comm_err_dict["ERR_QUERY_TERM"].format(ctx.author.mention))

            getattr(bill_item, query_cln_spl[0])

            query_category = query_cln_spl[0]
            query_item = query_cln_spl[1]

            return {"query_item": query_item, "query_category": query_category}
        except AttributeError:
            await ctx.channel.send(bill_comm_err_dict["ERR_INV_CAT"].format(ctx.author.mention))
        except Exception as e:
            raise BaseException(e)

    def update_billboard_items(self):
        h_soup = self.acquire_html(Request(url=hot_url, headers=hdr))
        b_soup = self.acquire_html(Request(url=bill200_url, headers=hdr))

        self.song_list.extend(self.get_list(h_soup))
        self.album_list.extend(self.get_list(b_soup))

        for song_idx, song in enumerate(self.song_list):
            self.song_list[song_idx] = SongInfo.from_billboard_item(song)

        for album_idx, album in enumerate(self.album_list):
            self.album_list[album_idx] = AlbumInfo.from_billboard_item(album)

    def acquire_html(self, request):
        url_str = urlopen(request)
        url_html = url_str.read()
        url_str.close()

        return soup(url_html, "html.parser")

    def get_list(self, html_soup):
        bi_list = []
        article_list = html_soup.find_all('li', class_='chart-list__element display--flex')

        for item in article_list:
            rank = item.find('span', class_="chart-element__rank__number").string.strip()
            name = item.find('span',
                             class_="chart-element__information__song text--truncate color--primary").string.strip()
            artists = item.find('span',
                                class_="chart-element__information__artist text--truncate color--secondary").string.strip()

            last_week, top_spot, weeks_on_chart, thumbnail_url = "--", "--", "--", "--"
            info_elem = item.find('div', class_="chart-element__metas display--flex flex--y-center")

            print(info_elem)

            if info_elem is not None:
                last_week = info_elem.find('div',
                                      class_="chart-element__meta text--center color--secondary text--last").string.strip()
                top_spot = info_elem.find('div',
                                     class_="chart-element__meta text--center color--secondary text--peak").string.strip()
                weeks_on_chart = info_elem.find('div',
                                           class_="chart-element__meta text--center color--secondary text--week").string.strip()

            thumbnail_url_elem = item.find('span', class_="chart-element__image flex--no-shrink")

            if thumbnail_url_elem is not None:
                if len(thumbnail_url_elem.attrs['style']) > 0:
                    thumbnail_url = thumbnail_url_elem.attrs['style'].split(": url(")[1][:-2]

            billboard_item_info = BillboardItem(rank, name, artists, last_week, top_spot, weeks_on_chart, thumbnail_url)
            bi_list.append(billboard_item_info)

        return bi_list


def setup(p_bot):
    p_bot.add_cog(Billboard(p_bot))