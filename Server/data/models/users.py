import datetime
import sqlalchemy
from ..check_db import SqlAlchemyBase
from sqlalchemy import orm

class users(SqlAlchemyBase):
    __tablename__ = 'users'
    id = sqlalchemy.Column(sqlalchemy.Integer,primary_key=True, autoincrement=True,unique=True)
    username = sqlalchemy.Column(sqlalchemy.String,nullable=True,unique=True)
    email = sqlalchemy.Column(sqlalchemy.String,nullable=True,unique=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String,nullable=True)
    creation_time = sqlalchemy.Column(sqlalchemy.DATETIME,nullable=True,default=datetime.datetime.now())
    icon = sqlalchemy.Column(sqlalchemy.String,nullable=True)
