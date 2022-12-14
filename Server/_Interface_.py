from PyQt5.QtWidgets import QMainWindow
from PyQt5 import uic


class AuthorizationsUser(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('Interface/Server.ui', self)
