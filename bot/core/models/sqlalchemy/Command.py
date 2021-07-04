from sqlalchemy import Column, Integer, String
from bot.core.startup import Base


class Command(Base):
    __tablename__ = "Command"
    id = Column(Integer, autoincrement=True, primary_key=True)
    command_id = Column(Integer, unique=True)
    name = Column(String)
