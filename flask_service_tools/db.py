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
    model = Column(String(255), nullable=False)
    task = Column(String(255), nullable=False)
    response_status = Column(String(20), nullable=False)
    prompt_tokens = Column(Integer, default=0)
    completion_tokens = Column(Integer, default=0)
    response_time_ms = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)


class DBManager:
    def __init__(self, db_config):
        self.engine = create_engine(
            f"mysql+pymysql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}",
            echo=False
        )
        self.Session = sessionmaker(bind=self.engine)

    def insert_usage_log(self, service_name, user_uuid, model, task, response_status, prompt_tokens, completion_tokens, response_time_ms):
        session = self.Session()
        try:
            usage_log = UsageLog(
                service_name=service_name,
                user_uuid=user_uuid,
                model=model,
                task=task,
                response_status=response_status,
                prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens,
                response_time_ms=response_time_ms
            )
            session.add(usage_log)
            session.commit()
        except SQLAlchemyError:
            session.rollback()
            raise
        finally:
            session.close()
