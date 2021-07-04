import sqlalchemy.engine
from sqlalchemy import (
    MetaData, Table, Column, Integer, String, Enum, Boolean
)
from sqlalchemy.engine import create_engine
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta
from sqlalchemy.orm import sessionmaker, mapper
from bot.core.config.Config import CoreConfig
from bot.core.models.Channel import Channel

engine: sqlalchemy.engine.Engine = create_engine(CoreConfig.get_connection_string())
engine.connect()
metadata = MetaData(engine)
Base: DeclarativeMeta = declarative_base(metadata=metadata)

channels = Table('channel', metadata,
                 Column('channel_id', Integer, primary_key=True),
                 Column('name', String(255)),
                 Column('type', Enum('voice', 'text')),
                 Column('is_nsfw', Boolean))

mapper(Channel, channels)
metadata.create_all(engine)
session_factory = sessionmaker(bind=engine)
