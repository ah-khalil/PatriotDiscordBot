import re
from entities.BillboardItem import BillboardItem


class SongInfo(BillboardItem):
    def __init__(self, rank, name, artist, features, lw_pos, pk_pos, ch_week, thumbnail_url):
        super(SongInfo, self).__init__(
            rank=rank,
            name=name,
            artist=artist,
            last_week=lw_pos,
            peak_pos=pk_pos,
            weeks_on_chart=ch_week,
            thumbnail_url=thumbnail_url
        )

        self._features = features

    def features_string(self):
        return ", ".join(str(x) for x in self.features) if (isinstance(self.features, list)) else "None"

    def to_string(self):
        return super(SongInfo, self).to_string() + "\n\tFeatures: " + self.features_string()

    @classmethod
    def from_billboard_item(self, billboard_item: BillboardItem):
        rank = billboard_item.rank
        name = billboard_item.name
        artists = billboard_item.artist
        peak_pos = billboard_item.peak_pos
        last_week = billboard_item.last_week
        week_on_ch = billboard_item.weeks_on_chart
        thumbnail_url = billboard_item._thumbnail_url

        feat_spl_arr = artists.split(" Featuring ")
        feature = re.split(" & | , ", feat_spl_arr[1]) if len(feat_spl_arr) > 1 else "None"

        return SongInfo(rank, name, feat_spl_arr[0], feature, last_week, peak_pos, week_on_ch, thumbnail_url)

    @property
    def features(self):
        return self._features

    @features.setter
    def features(self, value):
        self._features = value

    @features.deleter
    def features(self):
        del self._features
