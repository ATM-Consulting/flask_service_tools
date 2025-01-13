from sqlalchemy import create_engine, Column, String, Integer, Float, DateTime, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

Base = declarative_base()


class UsageLog(Base):
    __tablename__ = 'usage_logs'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    service_name = Column(String(255), nullable=False)
    user_uuid = Column(String(36))
    endpoint = Column(String(255), nullable=False)
    status_code = Column(Integer, nullable=False)
    tokens_consumed = Column(Integer, default=0)
    response_time_ms = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)


class DBManager:
    def __init__(self, db_config):
        self.engine = create_engine(
            f"mysql+pymysql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}",
            echo=False
        )
        self.Session = sessionmaker(bind=self.engine)

    def insert_usage_log(self, service_name, user_uuid, endpoint, status_code, tokens_consumed, response_time_ms):
        session = self.Session()
        try:
            usage_log = UsageLog(
                service_name=service_name,
                user_uuid=user_uuid,
                endpoint=endpoint,
                status_code=status_code,
                tokens_consumed=tokens_consumed,
                response_time_ms=response_time_ms
            )
            session.add(usage_log)
            session.commit()
        except SQLAlchemyError:
            session.rollback()
            raise
        finally:
            session.close()

# EXAMPLE
# from common_flask.db import DBManager
# from common_flask.config import Config
#
# db_manager = DBManager({
#     "host": Config.DB_HOST,
#     "port": Config.DB_PORT,
#     "user": Config.DB_USER,
#     "password": Config.DB_PASSWORD,
#     "database": Config.DB_NAME
# })
#
# db_manager.insert_usage_log(
#     service_name="customer_support",
#     user_id="user123",
#     endpoint="/api/v1/support",
#     status_code=200,
#     tokens_consumed=50,
#     response_time_ms=123.45
# )
