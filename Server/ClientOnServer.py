from threading import Thread
from Support import SortingListInDict
from REST_Commands import *
from pickle import dumps, loads
from forms_db import *
from db.bd_ import SelectMySqlConnection, InsertMySqlConnection
from struct import pack, unpack

connections = []


class Client(Thread):
    def __init__(self, socket):
        Thread.__init__(self, daemon=True)
        self.socket = socket
        self.signal = True
        self.Activated = False

    def Send_Data(self, data: dict) -> None:
        serialized_data = dumps(data)
        self.socket.sendall(pack('>I', len(serialized_data)))
        self.socket.sendall(serialized_data)

    def Receive_Data(self) -> dict:
        a = self.socket.recv(4)
        data_size = unpack('>I', a)[0]
        received_payload = b""
        reamining_payload_size = data_size
        while reamining_payload_size != 0:
            received_payload += self.socket.recv(reamining_payload_size)
            reamining_payload_size = data_size - len(received_payload)
        return loads(received_payload)

    def check_password(self, passwd_hash, password) -> bool:
        return password == passwd_hash

    def Insert_Data(self, form, *args, return_id=False, one_execut=True):
        with InsertMySqlConnection() as cur:
            if one_execut:
                cur.execute(form(), (*args,))
            else:
                cur.executemany(form(), (*args,))
            return cur._last_insert_id if return_id else None

    def Select_Data(self, form, *args, one_request=False) -> list:
        with SelectMySqlConnection() as cur:
            try:
                cur.execute(form(*args))
                if one_request:
                    return cur.fetchone()
                else:
                    return cur.fetchall()
            except Exception as e:
                print(form(*args),e)

    def Disconnect(self):
        self.signal = False
        connections.remove(self)


    def run(self):
        while self.signal:
            try:
                data_ = self.Receive_Data()
            except ConnectionError:
                return self.Disconnect()
            if not self.Activated:
                if data_['request'] == 'AUTHORIZATIONS':
                    self.Authorization(data_)
                elif data_['request'] == 'REGISTRATION':
                    self.Registration(data_)
            else:
                if data_['request'] == 'UPDATE':
                    self.Update(data_)
                elif data_['request'] == 'FIND':
                    self.FindUsers(data_)
                elif data_['request'] == 'CREATECHAT':
                    self.AddChat(data_)
                elif data_['request'] == 'MESSAGE':
                    self.Messega(data_)
                elif data_['request'] == 'UpdateIcon':
                    self.UpdateIcon(data_)
                elif data_['request'] == 'SignOut':
                    self.SignOut()

    def SignOut(self):
        self.Activated = False

    """Фунция авторизация пользователя"""

    def Authorization(self, data: dict):
        user = self.Select_Data(Get_User, data['username'], one_request=True)
        if user is None: return self.Send_Data(Error('ThereIsNoSuchName'))
        if not self.check_password(user[-2], data['password']): return self.Send_Data(Error('InvalidPassword'))
        self.Activated = True
        self.Send_Data(Ok_Authorization(user[0], user[1], user[2], user[-1]))
        return self.LoadChatsandUsers(user[0])

    """Фунция регистриции, нового пользователя"""

    def Registration(self, data: dict):
        user = self.Select_Data(Get_User, data['username'], one_request=True)
        if user is not None: return self.Send_Data(Error('NameAlreadyExists'))
        username, email, password, Icon = data['username'], data['email'], data[
            'password'], data['icon']
        self.Activated = True
        id = self.Insert_Data(Insert_Form_User, username, email, password, Icon,
                              return_id=True)
        return self.Send_Data(Ok_Registration(id, username, email))

    def Messega(self, data: dict):
        __data = list(data.values())[1:]
        self.Insert_Data(Insert_Form_Message, *__data)
        self.Send_Data(Message(__data[0], __data[2]))

    def UpdateIcon(self, data: dict):
        self.Insert_Data(UpdateIcomInDB, data['icon'], data['id_user'])
        return self.Send_Data(UpdateIconClient(data['icon']))

    def AddChat(self, data: dict):
        title, listusers, icon = data['title'], data['list_id_users'], data['icon']
        id = self.Insert_Data(Insert_Form_Chat, title, icon, return_id=True)
        id_chat_user = list(zip(listusers, [id] * len(listusers)))
        self.Insert_Data(Insert_Form_Chat_Participant, *id_chat_user, one_execut=False)

    """Фунция получения чатов и пользователей"""

    def LoadChatsandUsers(self, id: int):
        chats = self.Select_Data(Get_Chats, id)
        if not len(chats): return
        list_id_chat = list(map(lambda x: x[0], chats))
        users = self.Select_Data(Get_Users_In_Chat, list_id_chat, [id])
        messages = self.Select_Data(Get_Message_In_Chat, list_id_chat)
        messages = SortingListInDict(messages, 1) if messages != [] else {}
        if messages:
            for i in list_id_chat:
                if i not in messages.keys():
                    messages[i] = []
        users = SortingListInDict(users, 0) if users != [] else {}
        self.Send_Data(ListChatsAndUsers(users, messages, chats))

    """Фунция поиска пользователей"""

    def FindUsers(self, data: dict):
        users = self.Select_Data(Get_Find_Users, data['id_user'], data['SearchTarget'],
                                 one_request=False)
        self.Send_Data(FindUsers(users))

    def Update(self, data: dict):
        chats_id = data['chats_id']
        user_id = data['user_id']
        last_id_message_chat = data['last_id_message_chat']
        users, messages = {}, []
        chats = self.Select_Data(Get_Update_Chats, user_id, chats_id)
        if chats:
            list_id_chat = list(map(lambda x: x[0], chats))
            users = self.Select_Data(Get_Users_In_Chat, list_id_chat, data['users_id'])
        if chats_id:
            mes = self.Select_Data(Get_Find_Message_In_Chat, chats_id,user_id)
            messages = list(filter(lambda x: last_id_message_chat[x[1]] < x[0],mes))
        messages = SortingListInDict(messages, 1) if messages != [] else {}
        users = SortingListInDict(users, 0) if users != [] else {}
        self.Send_Data(UpdateChatsAndUsers(users, messages, chats))
