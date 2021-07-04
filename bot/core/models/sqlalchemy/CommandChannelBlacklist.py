# from sqlalchemy import Column, Integer, ForeignKey
# from sqlalchemy.orm import relationship, backref
# from bot.core.startup import Base
# from bot.core.models.sqlalchemy.Channel import Channel
#
#
# class CommandChannelBlacklist(Base):
#     __tablename__ = "CommandChannelBlacklist"
#     id = Column(Integer, autoincrement=True, primary_key=True)
#     command_id = Column(Integer, ForeignKey("command.id"))
#     channel_id = Column(Integer, ForeignKey("channel.id"))
#     command = relationship(Channel, backref=backref("CommandChannelBlacklist", cascade="all, delete-orphan"))
