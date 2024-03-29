import socket
from threading import Thread
import time
import ssl
import logging
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QListWidget, QListWidgetItem, \
    QLabel, QPlainTextEdit
from PyQt5.QtCore import pyqtSlot
from PyQt5 import uic
from data.db import *
from data.check_db import check_and_create_db
from config import *
from ClientOnServer import HandlerRequests, connections

def create_connect_db(file_name, max_queue_size=100):
    global db__
    db__ = Sqlite3Worker(file_name, max_queue_size=0)

class QTextEditLogger(logging.Handler):
    def __init__(self, parent: QListWidget):
        super().__init__()
        self.widget = parent

    def emit(self, record):
        msg = self.format(record)
        self.widget.addItem(QListWidgetItem(msg))


class ServerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.Connecting = QListWidget
        self.Status = QLabel
        self.setWindowTitle('ServerNewMess')
        uic.loadUi('Interface/Server.ui', self)
        self.Start.clicked.connect(self.Starting)
        self.Stop.clicked.connect(self.Stoping)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        self.context.load_cert_chain('Certificate/server.pem', 'Certificate/private_.key')
        self.Port.setText(str(port))
        self.IP_.setText(str(host))
        logTextBox = QTextEditLogger(self.logging__)
        logTextBox.setFormatter(
            logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        logging.getLogger().addHandler(logTextBox)
        logging.getLogger().setLevel(logging.DEBUG)
        self.Address_2.setText(f'{host}:{port}')
        self.Disable()

    def ConfigServerSocket(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        self.context.load_cert_chain('Certificate/server.pem', 'Certificate/private_.key')
        self.sock.bind((host, port))
        self.sock.listen(20)
        self.ssock = self.context.wrap_socket(self.sock, server_side=True)

    def Disable(self):
        self.ActServer = False
        self.Status.setText('Disable')
        self.Status.setStyleSheet("color:red")

    def Stoping(self):
        try:
            self.sock.close()
            db__ == None
            [i.Disconnect() for i in connections]
            self.conn = None
            self.Disable()
        except Exception:
            pass

    def Starting(self):
        try:
            if not self.ActServer:
                
                self.ConfigServerSocket()
                self.ActServer = True
                self.conn = Thread(target=self.newConnections, args=(self.ssock,))
                self.conn.start()
                logging.info(f"Starting server: {host}:{port}.")
                db_puth = 'db/ServerBaseDate.db'
                check_and_create_db(db_puth)
                create_connect_db(db_puth)
            else:
                logging.error(f"A server is already running")
        except Exception as e:
            logging.error(f"Error when starting the server: {e}.")

    def newConnections(self, socket):
        self.Status.setText('Active')
        self.Status.setStyleSheet("color:green")
        while self.ActServer:
            try:
                sock, address = socket.accept()
                print(1)
                connections.append(HandlerRequests(sock,db__))
                connections[-1].start()
                time.sleep(0.01)
                logging.info(f"Connection: {address}.")
            except ssl.SSLError as e:
                logging.error(f"ConnectionError: {e}.")
            except Exception as e:
                logging.error(f"Error: {e}.")



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ServerInt = ServerApp()
    ServerInt.show()
    sys.exit(app.exec_())
