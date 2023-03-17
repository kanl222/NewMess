from time import sleep
from struct import pack
from PyQt5.QtCore import QThread,pyqtSignal
from pickle import dumps
from forms import Update,Error_Connect_Server


# Мониторинг новых сообщений
class new_message_monitor(QThread):
    server_socket = None
    mysignal = pyqtSignal(int)

    def __init__(self, parent=None):
        QThread.__init__(self, parent)
        self.id = 0
        self.chatsid = []
        self.last_message_chats = {}
        self.users_id = []

    def Send_Data(self, data):
        try:
            serialized_data = dumps(data)
            self.server_socket.sendall(pack('>I', len(serialized_data)))
            self.server_socket.sendall(serialized_data)
        except Exception:
            self.mysignal.emit(4004)
            self.quit()

    def run(self):
        try:
            while True:
                self.sleep(2)
                if self.server_socket != None:
                    self.Send_Data(
                        Update(self.chatsid, self.last_message_chats, self.users_id,
                               self.id))
        except Exception:
            pass

    def Update_id(self, id: int):
        self.id = id

    def update_list(self, chatsid, last_message_chats, users_id):
        self.chatsid, self.last_message_chats, self.users_id = chatsid, last_message_chats, users_id
