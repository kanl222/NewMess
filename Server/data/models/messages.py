import datetime
import sqlalchemy
from ..check_db import SqlAlchemyBase
from sqlalchemy import orm

class messages(SqlAlchemyBase):
    __tablename__ = 'messages'
    id = sqlalchemy.Column(sqlalchemy.Integer,primary_key=True,autoincrement=True,nullable=True,unique=True)
    id_user = sqlalchemy.Column(sqlalchemy.Integer,sqlalchemy.ForeignKey("users.id"),nullable=True)
    id_chat = sqlalchemy.Column(sqlalchemy.Integer,sqlalchemy.ForeignKey("chats.id"),nullable=True)
    message = sqlalchemy.Column(sqlalchemy.String,nullable=True)
    send_time_message = sqlalchemy.Column(sqlalchemy.DATETIME,nullable=True,default=datetime.datetime.now())
    
