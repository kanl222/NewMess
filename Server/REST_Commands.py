def Invalid_Key():
    return {
        'command': 'INVALID_KEY',
    }


def Cheked_Key():
    return {
        'command': 'CHEKED_KEY',
    }


def Update_key_sipher(key):
    return {
        'command': 'UPDATE_KEY_SIPHER',
        'key_sipher': key
    }


def Ok_Authorization(_id: int, username: str, email: str, icon: str) -> dict:
    return {
        'command': 'OK_AUTHORIZATION',
        'id': _id,
        'username': username,
        'email': email,
        'icon': icon
    }


def Ok_Registration(_id: int, username: str, email: str) -> dict:
    return {
        'command': 'OK_REGISTRATION',
        'id': _id,
        'username': username,
        'email': email,
    }


def Error(Error: str) -> dict:
    return {
        'command': 'error',
        'error': Error
    }


def FindUsers(Users: list) -> dict:
    return {
        'command': 'USERSFIND',
        'listusers': Users
    }


def ListChatsAndUsers(users: dict, messages: dict, chats: list) -> dict:
    return {
        'command': 'LISTCHATSANDUSERS',
        'users': users,
        'messages': messages,
        'chats': chats
    }
def UpdateChatsAndUsers(users: dict, messages: dict, chats: list) -> dict:
    return {
        'command': 'UPDATE',
        'users': users,
        'messages': messages,
        'chats': chats
    }

def Message(id_chat:int,message:str) -> dict:
    return {
        'command': 'MESSAGE',
        'id_chat': id_chat,
        'message':message
    }



def UpdateIconClient(icon) -> dict:
    return {
        'command': 'UPDATEICONCLIENT',
        'icon': icon,
    }