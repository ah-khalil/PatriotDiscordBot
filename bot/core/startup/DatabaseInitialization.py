# import sqlalchemy
#
# from sqlalchemy import MetaData
# from sqlalchemy.engine import create_engine
# from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta
# from bot.core.config.Config import CoreConfig
# from sqlalchemy.orm import scoped_session, sessionmaker
# from sqlalchemy.engine import Engine
#
# Base: DeclarativeMeta = declarative_base()
#
#
# def init_session():
#     engine: Engine = create_engine(CoreConfig.get_connection_string())
#     engine.connect()
#     metadata = MetaData(engine)
#     session_factory: sessionmaker = sessionmaker(bind=engine)
#
#     return session_factory
