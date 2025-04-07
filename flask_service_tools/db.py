from sqlalchemy import create_engine, Column, String, Float, BigInteger, Table, MetaData, and_
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
            result = session.execute(insert_stmt)
            session.commit()
            inserted_id = result.inserted_primary_key[0] if result.inserted_primary_key else 0
            return inserted_id
        except SQLAlchemyError as e:
            session.rollback()
            return e
        finally:
            session.close()

    def select_custom_logs(self, table_name, filters=None):
        session = self.Session()
        try:
            metadata = MetaData()
            custom_table = Table(table_name, metadata, autoload_with=self.engine)
            query = session.query(custom_table)
            if filters:
                conditions = [custom_table.c[key] == value for key, value in filters.items()]
                query = query.filter(and_(*conditions))
            results = query.all()
            return [dict(row._mapping) for row in results]
        except SQLAlchemyError as e:
            return e
        finally:
            session.close()

    def update_custom_logs(self, table_name, filters, update_values):
        session = self.Session()
        try:
            metadata = MetaData()
            custom_table = Table(table_name, metadata, autoload_with=self.engine)
            conditions = [custom_table.c[key] == value for key, value in filters.items()]
            update_stmt = custom_table.update().where(and_(*conditions)).values(**update_values)
            result = session.execute(update_stmt)
            session.commit()
            return result.rowcount
        except SQLAlchemyError as e:
            session.rollback()
            return e
        finally:
            session.close()

# Examples
#
# logs = db.select_custom_logs('custom_log_table', filters={"user_uuid": "abc-123"})
#
# updated_count = db.update_custom_logs(
#     'custom_log_table',
#     filters={"user_uuid": "abc-123"},
#     update_values={"response_status": "success"}
# )
