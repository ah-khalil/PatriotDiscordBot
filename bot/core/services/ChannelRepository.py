from bot.core.services.EntityRepository import EntityRepository
from bot.core.models.Channel import Channel


class ChannelRepository(EntityRepository[Channel]):
    def __init__(self):
        super(ChannelRepository, self).__init__()
        self._channel_query = self.session.query(Channel)

    def add(self, channel_id: int, channel: Channel = None, **kwargs):
        if channel is not None:
            self.session.add(channel)
        else:
            channel_name = kwargs["name"]
            channel_type = kwargs["type"]
            channel_nsfw = kwargs["is_nsfw"]

            self.session.add(
                Channel(channel_id, channel_name, channel_type, channel_nsfw))

        self.session.commit()

    def update(self, channel: Channel):
        self._channel_query.filter(channel_id=channel.channel_id).update({
            "channel_id": channel.channel_id,
            "name": channel.name,
            "type": channel.type,
            "is_nsfw": channel.is_nsfw
        })

    def delete(self, channel: Channel):
        self.session.delete(channel)

    def get(self, channel: Channel):
        return self._channel_query.get(channel.channel_id)

    def exists(self, channel: Channel) -> bool:
        return self._channel_query.filter(channel_id=channel.channel_id).scalar()
