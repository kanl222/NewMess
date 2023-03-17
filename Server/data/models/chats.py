import datetime
import sqlalchemy
from ..check_db import SqlAlchemyBase
from sqlalchemy import orm

class Chats(SqlAlchemyBase):
    __tablename__ = 'chats'
    id = sqlalchemy.Column(sqlalchemy.Integer,primary_key=True,autoincrement=True,nullable=True,unique=True)
    tittle = sqlalchemy.Column(sqlalchemy.String,nullable=True,unique=True)
    icon = sqlalchemy.Column(sqlalchemy.LargeBinary,nullable=True)


