from entities.BillboardItem import BillboardItem

class AlbumInfo(BillboardItem):
    def __init__(self, rank, name, artist, last_week, peak_pos, weeks_on_chart, thumbnail_url):
        super(AlbumInfo, self).__init__(
            rank=rank,
            name=name,
            artist=artist,
            last_week=last_week,
            peak_pos=peak_pos,
            weeks_on_chart=weeks_on_chart,
            thumbnail_url=thumbnail_url
        )

    @classmethod
    def from_billboard_item(self, billboard_item: BillboardItem):
        rank = billboard_item.rank
        name = billboard_item.name
        artists = billboard_item.artist
        peak_pos = billboard_item.peak_pos
        last_week = billboard_item.last_week
        week_on_ch = billboard_item.weeks_on_chart
        thumbnail_url = billboard_item._thumbnail_url

        return AlbumInfo(rank, name, artists, last_week, peak_pos, week_on_ch, thumbnail_url)