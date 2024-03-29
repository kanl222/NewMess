def Get_ID_User(username:str,email:str) -> str:
    return f"SELECT id FROM Users WHERE username = '{username}' or email = '{email}';"

def Insert_Form_User() -> str:
    return "insert into Users(username,email,hashed_password,creation_time,icon) values (?,?,?,?,?)"


def Insert_Form_Chat() -> str:
    return "insert into chats(title,icon) values (?,?)"


def Insert_Form_Chat_Participant() -> str:
    return "insert into chat_participants(id_chat,id_user) values (?,?)"


def Insert_Form_Message() -> str:
    return "insert into message(id_user,id_chat,message,send_time_message) values (?,?,?,?)"


def Insert_Form_Session(**kwargs) -> str:
    return f"insert into Session values (Null,{kwargs['id_user']},'{kwargs['key_session']}')"


def Get_User(username: str) -> str:
    return f"SELECT * FROM Users WHERE username = '{username}';"


def Get_Id_User(username: str) -> str:
    return f"SELECT id FROM Users WHERE username = '{username}'"

def Get_Id_Chat(username: str) -> str:
    return f"SELECT id FROM Users WHERE username = '{username}'"


def Get_Find_Users(id_user: int, find: str) -> str:
    return "SELECT id,username FROM Users WHERE username LIKE '%{0}%' AND id != {1};".format(
        find, id_user)


def Get_Chats(id_user: int) -> str:
    return "SELECT * From chats WHERE id In(SELECT id_chat From chat_participants WHERE id_user = {0});".format(
        id_user)


def Get_Users_In_Chat(id_chats_list: list, id_users: list) -> str:
    return "SELECT id,username,icon From Users WHERE id IN (SELECT DISTINCT id_user From chat_participants WHERE id_chat In ({0}) AND id_user not in ({1}));".format(
        ', '.join(list(map(str, id_chats_list))), ', '.join(list(map(str, id_users))))


def Get_Message_In_Chat(id_chats_list: list) -> str:
    return "SELECT * From message WHERE chat_id IN ({0});".format(
        ', '.join(list(map(str, id_chats_list))))


def Get_Find_Message_In_Chat(chats_id:list,user_id:int) -> str:
    return "SELECT * From message Where chat_id In ({0}) And user_id != {1};".format(', '.join(list(map(str, chats_id))),user_id)

def Get_Update_Chats(id_user: int,list_chat_id:list) -> str:
    if list_chat_id:
        return "SELECT * From chats WHERE id In(SELECT id_chat From chat_participants WHERE id_user = {0} AND id_chat not in ({1}));".format(id_user,', '.join(list(map(str, list_chat_id))))
    return "SELECT * From chats WHERE id In(SELECT id_chat From chat_participants WHERE id_user = {0});".format(id_user)

def UpdateIcomInDB():
    return """UPDATE Users SET icon=? WHERE id = ?;"""

