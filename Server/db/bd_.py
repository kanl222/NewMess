import Server.config as config
import threading
import mysql.connector

class SelectMySqlConnection(object):
    def __init__(self, dburi=None):
        self.lock = threading.Lock()
        self.connection = mysql.connector.connect(host="localhost",    # your host, usually localhost
                            user="root",         # your username
                            passwd="MariaDB",  # your passworde
                            database="chatmenager")        # name of the data bas
        self.cursor = None
    def __enter__(self):
        self.lock.acquire()
        self.cursor = self.connection.cursor(buffered=True)
        return self.cursor

    def __exit__(self, type, value, traceback):
        self.lock.release()
        self.cursor.close()
        self.connection.close()


class InsertMySqlConnection(object):
    def __init__(self, dburi=None):
        self.lock = threading.Lock()
        self.connection = mysql.connector.connect(host="localhost",    # your host, usually localhost
                            user="root",         # your username
                            passwd="MariaDB",  # your passworde
                            database="chatmenager")
        self.cursor = None

    def __enter__(self):
        self.lock.acquire()
        self.cursor = self.connection.cursor()
        return self.cursor

    def __exit__(self, type, value, traceback):
        self.lock.release()
        self.connection.commit()
        self.cursor.close()
        self.connection.close()