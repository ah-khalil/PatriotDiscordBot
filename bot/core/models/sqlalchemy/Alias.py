from bot.core.startup import Base
from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint


class Alias(Base):
    __tablename__ = "Alias"
    id = Column(Integer, autoincrement=True, primary_key=True)
    command_id = Column(Integer, ForeignKey("command.id"))
    name = Column(String, UniqueConstraint("command_id"))
