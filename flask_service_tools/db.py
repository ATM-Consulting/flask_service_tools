from sqlalchemy import create_engine, Column, String, Float, BigInteger, Table, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

Base = declarative_base()


class UsageLog(Base):
    __tablename__ = 'usage_logs'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    service_name = Column(String(255), nullable=False)
    user_uuid = Column(String(36))
    task = Column(String(255), nullable=False)
    response_status = Column(String(20), nullable=False)
    response_time_ms = Column(Float, nullable=False)


class DBManager:
    def __init__(self, db_config):
        self.engine = create_engine(
            f"mysql+pymysql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}",
            echo=False
        )
        self.Session = sessionmaker(bind=self.engine)

    def insert_usage_log(self, service_name, user_uuid, task, response_status, response_time_ms):
        session = self.Session()
        try:
            usage_log = UsageLog(
                service_name=service_name,
                user_uuid=user_uuid,
                task=task,
                response_status=response_status,
                response_time_ms=response_time_ms
            )
            session.add(usage_log)
            session.commit()
            return usage_log.id
        except SQLAlchemyError as e:
            session.rollback()
            return e
        finally:
            session.close()

    def insert_custom_data(self, table_name, data):
        session = self.Session()
        try:
            metadata = MetaData()
            custom_table = Table(table_name, metadata, autoload_with=self.engine)
            insert_stmt = custom_table.insert().values(**data)
            session.execute(insert_stmt)
            session.commit()
            return True
        except SQLAlchemyError as e:
            session.rollback()
            return e
        finally:
            session.close()
