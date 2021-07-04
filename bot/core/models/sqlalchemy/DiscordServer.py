from bot.core.startup import Base
from sqlalchemy import Column, Integer


class DiscordServer(Base):
    __tablename__ = "Discord_Server"
    id = Column(Integer, autoincrement=True, primary_key=True)
    server_id = Column(Integer, unique=True)
