import sqlite3

sqlite3.SQLITE_OPEN_NOMUTEX()
connection = sqlite3.connect('BaseDate.db',timeout=20,check_same_thread=True)
print(connection)