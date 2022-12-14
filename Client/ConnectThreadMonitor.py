from pickle import dumps, loads
from struct import unpack,pack
from PyQt5.QtCore import QThread,pyqtSignal


# Мониторинг входящих сообщений
class message_monitor(QThread):
    server_socket = None
    mysignal = pyqtSignal(dict)

    def __init__(self, parent=None):
        QThread.__init__(self, parent)
        self.Activated = False

    def InfoSend(self,data,serialized_data):
        print('==================================')
        print(data)
        i = pack('>I', len(serialized_data))
        print(i)
        print(unpack('>I', i))
        print('===============================')

    def Send_Data(self, data):
        serialized_data = dumps(data)
        self.InfoSend(data,serialized_data)
        self.server_socket.sendall(pack('>I', len(serialized_data)))
        self.server_socket.sendall(serialized_data)

    def Receive_Data(self) -> dict:
        try:
            data_size = unpack('>I', self.server_socket.recv(4))[0]
            received_payload = b""
            reamining_payload_size = data_size
            while reamining_payload_size != 0:
                received_payload += self.server_socket.recv(reamining_payload_size)
                reamining_payload_size = data_size - len(received_payload)
            return loads(received_payload)
        except Exception:
            self.exit()

    def run(self):
        try:
            while True:
                if self.server_socket != None:
                    message = self.Receive_Data()
                    if message is not None:
                        self.mysignal.emit(message)
        except Exception as e:
            print(e)

    # Отправить зашифрованное сообщение на сервер
    def send(self, data_list: dict):
        self.Send_Data(data_list)
