import datetime
import sqlalchemy
from ..check_db import SqlAlchemyBase
from sqlalchemy import orm

class chats_participants(SqlAlchemyBase):
    __tablename__ = 'chat_participants'
    id = sqlalchemy.Column(sqlalchemy.Integer,primary_key=True,autoincrement=True,nullable=True,unique=True)
    id_chat = sqlalchemy.Column(sqlalchemy.Integer,sqlalchemy.ForeignKey("chats.id"),nullable=True,)
    id_user = sqlalchemy.Column(sqlalchemy.Integer,sqlalchemy.ForeignKey("users.id"),nullable=True)
    icon = sqlalchemy.Column(sqlalchemy.String,nullable=True)


