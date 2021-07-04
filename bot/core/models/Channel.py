# from bot.core.startup import engine, Base, metadata
# from sqlalchemy import Column, Integer, String, Boolean, Enum
# from sqlalchemy.orm import relationship


# class Channel(Base):
#     __tablename__ = "Channel"
#     id = Column(Integer, autoincrement=True, primary_key=True)
#     channel_id = Column(Integer, unique=True)
#     name = Column(String)
#     type = Column(Enum("Voice", "Text"))
#     is_nsfw = Column(Boolean)
#     # blacklisted_commands = relationship(
#     #     "Channel", secondary="CommandChannelBlacklist", back_populates="channels"
#     # )
#
#     def __init__(self):
#         pass
#
#     def __change_name(self, name: str):
#         self.name = name

class Channel:
    def __init__(self, channel_id, name, channel_type, is_nsfw):
        self.channel_id = channel_id
        self.name = name
        self.type = channel_type
        self.is_nsfw = is_nsfw

    def change_name(self, name: str):
        self.name = name
