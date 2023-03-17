from config import salt
from datetime import datetime
import hashlib
import base64

format = "%Y-%m-%d %H:%M"


def Sending_The_Key(key) -> dict:
    return {
        'request': 'CHEKIN_KEY',
        'key': key
    }


def Authorizations(name: str, password_: str) -> dict:
    return {
        'request': 'AUTHORIZATIONS',
        'username': name,
        'password': hashlib.pbkdf2_hmac('sha256', password_.encode('utf-8'), salt,
                                        100000).hex()
    }


def Registration(name: str, email: str, password: str, icon: base64) -> dict:
    return {
        'request': 'REGISTRATION',
        'username': name,
        'email': email,
        'password': hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt,100000).hex(),
        'icon': icon
    }


def Update(chats_id: list, last_id_message_chat: dict, users_id: list,
           user_id: int) -> dict:
    return {
        'request': 'UPDATE',
        'chats_id': chats_id,
        'last_id_message_chat': last_id_message_chat,
        'users_id': users_id,
        'user_id': user_id
    }


def SendMessage(id_user: int, id_chat: int, message: str) -> dict:
    time = datetime.now()
    return {
        'request': 'MESSAGE',
        'id_user': id_chat,
        'id_chat': id_user,
        'message': message,
        'datetime': time.strftime(format)
    }


def ERROR_Connect() -> dict:
    return {
        'error': 'ERROR_CONNECT_TO_SERVEr',
    }


def Find_Users(id_user: int, SearchTarget: str) -> dict:
    return {
        'request': 'FIND',
        'id_user': id_user,
        'SearchTarget': SearchTarget
    }


def CreateChat(title: str, listidusers: list, Icon: base64) -> dict:
    return {
        'request': 'CREATECHAT',
        'title': title,
        'list_id_users': listidusers,
        'icon': Icon
    }


def UpdateIconUser(id_: int, Icon: base64) -> dict:
    return {
        'request': 'UpdateIcon',
        'id_user': id_,
        'icon': Icon
    }


def Error_Connect_Server() -> dict:
    return {
        'command': 'error',
        'error': 'ERROR_CONNECT_TO_SERVER'
    }


def SignOut() -> dict:
    return {
        'request': 'SignOut'
    }
