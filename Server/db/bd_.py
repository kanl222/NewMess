
import threading
import sqlite3

class SelectMySqlConnection(object):
    def __init__(self, dburi=None):
        self.lock = threading.Lock()
        self.connection = sqlite3.connect('db/BaseDate.db',timeout=20,check_same_thread=True)       # name of the data bas
        self.cursor = None
    def __enter__(self):
        self.lock.acquire()
        self.cursor = self.connection.cursor()
        return self.cursor

    def __exit__(self, type, value, traceback):
        self.lock.release()
        self.cursor.close()
        self.connection.close()


class InsertMySqlConnection(object):
    def __init__(self, dburi=None):
        self.lock = threading.Lock()
        self.connection = sqlite3.connect('db/BaseDate.db',timeout=20,check_same_thread=True)
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