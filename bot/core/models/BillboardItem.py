import re
import abc


class BillboardItem:
    def __init__(self, rank, name, artist, last_week, peak_pos, weeks_on_chart, thumbnail_url):
        self._rank = rank
        self._name = name
        self._artist = artist
        self._peak_pos = peak_pos
        self._last_week = last_week
        self._weeks_on_chart = weeks_on_chart
        self._thumbnail_url = thumbnail_url

    def to_string(self):
        return "\nRank: " + self._rank + "\n\tName: " + self._name + "\n\tArtist: " + self._artist + "\n\tLast Week Pos: " + str(
            self._last_week) + "\n\tPeak Position: " + str(self._peak_pos) + "\n\tWeek on Chart: " + str(
            self._weeks_on_chart)

    def from_billboard_item(self, billboard_item):
        pass

    @property
    def rank(self):
        return self._rank

    @rank.setter
    def rank(self, value):
        self._rank = value

    @rank.deleter
    def rank(self):
        del self._rank

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @name.deleter
    def name(self):
        del self._name

    @property
    def artist(self):
        return self._artist

    @artist.setter
    def artist(self, value):
        self._artist = value

    @artist.deleter
    def artist(self):
        del self._artist

    @property
    def peak_pos(self):
        return self._peak_pos

    @peak_pos.setter
    def peak_pos(self, value):
        self._peak_pos = value

    @peak_pos.deleter
    def peak_pos(self):
        del self._peak_pos

    @property
    def last_week(self):
        return self._last_week

    @last_week.setter
    def last_week(self, value):
        self._last_week = value

    @last_week.deleter
    def last_week(self):
        del self._last_week

    @property
    def weeks_on_chart(self):
        return self._weeks_on_chart

    @weeks_on_chart.setter
    def weeks_on_chart(self, value):
        self._weeks_on_chart = value

    @weeks_on_chart.deleter
    def weeks_on_chart(self):
        del self._weeks_on_chart

    def get_thumbnail_url(self):
        return self._thumbnail_url
