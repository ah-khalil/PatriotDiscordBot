# from sqlalchemy import Column, Integer, ForeignKey
# from sqlalchemy.orm import relationship, backref
#
# from bot.core.startup import Base
# from bot.core.models.sqlalchemy.User import User
#
#
# class CommandUserBlacklist(Base):
#     __tablename__ = "CommandUserBlacklist"
#     id = Column(Integer, autoincrement=True, primary_key=True)
#     command_id = Column(Integer, ForeignKey("command.id"))
#     user_id = Column(Integer, ForeignKey("user.id"))
#     user = relationship(User, backref=backref("CommandUserBlacklist", cascade="all, delete-orphan"))
