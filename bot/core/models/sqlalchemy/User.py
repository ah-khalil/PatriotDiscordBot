from bot.core.startup import Base
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "User"
    id = Column(Integer, autoincrement=True, primary_key=True)
    user_id = Column(Integer, unique=True)
    name = Column(String)
    is_bot = Column(Boolean)
    date_created = Column(DateTime)
    # blacklisted_commands = relationship(
    #     "Command", secondary="CommandUserBlacklist", back_populates="users"
    # )
