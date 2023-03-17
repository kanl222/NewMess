import sqlalchemy as sa
import logging
import sqlalchemy.ext.declarative as dec
from os import path
import sqlite3
SqlAlchemyBase = dec.declarative_base()


def check_and_create_db(db_file):
    if not db_file or not db_file.strip():
        raise Exception("Необходимо указать файл базы данных.")
    if not path.exists(db_file):
        logging.error('Состояние базы данных : не была найдена ')
        logging.debug('Создание базы данных.......')
        conn_str = f'sqlite:///{db_file.strip()}?check_same_thread=False'
        from . import __all_models
        engine = sa.create_engine(conn_str, echo=False)
        SqlAlchemyBase.metadata.create_all(engine)
        return logging.debug('База данных создана')
    return logging.debug('Состояние базы данных: ok')
    