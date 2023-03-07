import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm

class Chats(SqlAlchemyBase):
    __tablename__ = 'chats'
    id = sqlalchemy.Column(sqlalchemy.Integer,primary_key=True,nullable=True)
    tittle = sqlalchemy.Column(sqlalchemy.String,nullable=True)
    chat_participant = sqlalchemy.Column(sqlalchemy.BLOB,nullable=True)
    icon = sqlalchemy.Column(sqlalchemy.String,nullable=True)


class messages(SqlAlchemyBase):
    __tablename__ = 'messages'
    id_messages = sqlalchemy.Column(sqlalchemy.Integer,primary_key=True,nullable=True)
    id_user = sqlalchemy.Column(sqlalchemy.Integer,nullable=True)
    id_chat = sqlalchemy.Column(sqlalchemy.Integer,nullable=True)
    message = sqlalchemy.Column(sqlalchemy.String,nullable=True)

class users(SqlAlchemyBase):
    __tablename__ = 'users'
    id = sqlalchemy.Column(sqlalchemy.Integer,primary_key=True,nullable=True)
    username = sqlalchemy.Column(sqlalchemy.String,nullable=True)
    icon = sqlalchemy.Column(sqlalchemy.String,nullable=True)

