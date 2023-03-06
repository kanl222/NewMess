from PyQt5.QtWidgets import QApplication, QDesktopWidget, QWidget, QStackedWidget
from interface import MyChatsManager, RegistrationWindow, AuthorizationsUser
from InterfaceData.Painter.PaintAndMask import CtreateAvatar
from UpdateThreadMessage import new_message_monitor
from ConnectThreadMonitor import message_monitor
from ssl import SSLContext,PROTOCOL_TLSv1
from Support import PixmapToBase64,list_id
from PyQt5.QtGui import QIcon
from threading import Thread
from socket import socket,AF_INET,SOCK_STREAM
from PyQt5.Qt import Qt
from PyQt5.QtCore import QPoint
from time import sleep
from config import *
from forms import *
import sys


class LocalClient(object):
    def __init__(self):
        self.hostname = 'www.newmess.com'
        self.context = SSLContext(PROTOCOL_TLSv1)
        self.context.load_verify_locations('Certificate/server.pem')
        self.ConfigClient()

        #Подключаем обработчики
        self.connect_monitor = message_monitor()
        self.new_message = new_message_monitor()
        self.new_message.mysignal.connect(self.Error_System)
        self.connect_monitor.mysignal.connect(self.signal_handler)
        self.connect_to_server()

    def ConfigClient(self):
        self.Activated = False

        self.name = ''
        self.email = ''
        self.icon = ''

        self.chats = []
        self.message_chats = {}
        self.users = {}

        self.chatsid = list_id()
        self.last_message_chats = {}
        self.users_id = list_id()

    def Icon(self, src):
        with open(src, "rb", ) as image:
            return base64.b64encode(image.read())

    def signal_handler(self, value: dict) -> None:
        if value['command'] == 'error':
            return self.Error_handler(value)
        return self.Command_handler(value)

    def Reconnect(self):
        try:
            if self.connect_monitor.isRunning():
                self.connect_monitor.terminate()
            if self.new_message.isRunning():
                self.new_message.terminate()
            self.connect_monitor = message_monitor()
            self.new_message = new_message_monitor()
            self.connect_to_server()
        except Exception as e:
            print(e,2)

    def Error_System(self,CodeError:int):
        if CodeError == 4004:
            pass
            # return self.Reconnect()

    def Error_handler(self, error: dict) -> None:
        if error['error'] == 'ThereIsNoSuchName':
            return loginform.Error_mes('Нет аккаунта с таким именем пользователя')
        if error['error'] == 'InvalidPassword':
            return loginform.Error_mes('Вы ввели неверный пароль')
        if error['error'] == 'NameAlreadyExists':
            return registerform.Error_mes('Tакое имя уже существует')

    def Command_handler(self, data: dict) -> None:
        print(data)
        if not self.Activated:
            if data['command'] in ('OK_AUTHORIZATION', 'OK_REGISTRATION'):
                try:
                    self.Activated = True
                    self.id = data['id']
                    self.name = data['username']
                    self.email = data['email']
                    self.users_id = [self.id]
                    if data['command'] == 'OK_AUTHORIZATION':
                        self.UpdateIcon(data['icon'])
                    else:
                        chatform.setIconUser(self.icon)
                        self.new_message.start()
                    chatform.Update_config(data['id'], data['username'], data['email'],self.icon)
                    self.new_message.Update_id(self.id)
                    widget.LaunchMyChat()
                    return
                except Exception as e:
                    print(e)
        else:
            try:
                print(data)
                if data['command'] == 'USERSFIND':
                    return chatform.CreateChat.Find_Handler(data['listusers'])
                if data['command'] == 'LISTCHATSANDUSERS':
                    self.chats = data['chats']
                    self.message_chats = data['messages']
                    self.users = data['users']
                    self.Update_list_id()
                    self.new_message.start()
                    return chatform.LoadChats()
                if data['command'] == 'UPDATE':
                    Thread(target=self.Handler_update,args=(data,chatform)).run()
                if data['command'] == 'MESSAGE':
                    return self.AddMessage(data)

                if data['command'] == 'UPDATEICONCLIENT':
                    return self.UpdateIcon(data['icon'])
            except Exception:
                pass

    def UpdateIcon(self,icon:base64):
        self.icon = icon
        chatform.setIconUser(self.icon)


    def AddMessage(self, data):
        try:
            self.message_chats[data['id_chat']] += [('', '', self.id, data['message'])]
            chatform.Add_message(self.name, data['message'], self.icon)
        except Exception as e:
            print(e)

    def Handler_update(self, data,chatform):
            if data['chats']:
                [self.AddChat(i) for i in data['chats']]
                if data['users']:  self.users |= data['users']
            if data['messages']:
                [self.message_chats[i].append(item) for i in data['messages'].keys() for
                 item in data['messages'][i]]
                for i in data['messages'].keys():
                    if chatform.Id_chat == i:
                        for message in data['messages'][i]:
                            _, username, icon = self.users[message[2]][0]
                            chatform.Add_message(username, message[3], icon)
            if data['chats'] or data['messages'] or data['users']: self.Update_list_id()


    def Update_list_id(self):
            self.chatsid += [x[0] for x in self.chats if x[0] not in self.chatsid]
            for i in self.chatsid:
                if i in self.message_chats.keys():
                    messages = list(filter(lambda x: x[2] != self.id, self.message_chats[i]))
                    if messages:
                        self.last_message_chats[i] = max(messages, key=lambda x: x[0])[0]
                    else:
                        self.last_message_chats[i] = 0
            self.users_id |= list_id(self.users.keys())
            self.new_message.update_list(self.chatsid.to_list(), self.last_message_chats,self.users_id)

    def AddChat(self,item):
        self.chats.append(item)
        chatform.Add_Chat_In_Menu(*item)
        self.message_chats[item[0]] = []


    def connect_to_server(self):
        try:
            self.sock_ = socket(AF_INET, SOCK_STREAM)
            self.sock_.connect((host, port))
            self.sock = self.context.wrap_socket(self.sock_, server_hostname=self.hostname)

            # Запускаем мониторинги входящих сообщений
            self.connect_monitor.server_socket = self.sock
            self.new_message.server_socket = self.sock
            self.connect_monitor.start()
        except Exception:
            sleep(5)
            self.connect_to_server()

    def Sending_request_data(self, form, **kwargs) -> None:
        try:
            if form == 'Authorizations':
                name, password = kwargs['name'], kwargs['password']
                return self.connect_monitor.send(Authorizations(name, password))
            if form == 'Registration':
                name, email, password = kwargs['name'], kwargs['email'], kwargs[
                    'password']
                self.icon = PixmapToBase64(CtreateAvatar(name))
                return self.connect_monitor.send(
                    Registration(name, email, password, self.icon))
            if form == 'Message':
                id_chat, mes = kwargs['id_chat'], kwargs['message']
                return self.connect_monitor.send(
                    SendMessage(self.id, id_chat, mes))
            if form == 'Find':
                mes = kwargs['SearchTarget']
                return self.connect_monitor.send(Find_Users(self.id, mes))
            if form == 'CreateChat':
                title, ListIdUsers,icon = kwargs['title'], kwargs['ListIdUsers'],kwargs['Icon']
                if not icon:
                    icon = PixmapToBase64(CtreateAvatar(title))
                ListIdUsers.append(self.id)
                return self.connect_monitor.send(CreateChat(title, ListIdUsers,icon))
            if form == 'UpdateIconUser':
                icon = kwargs['Icon']
                return self.connect_monitor.send(UpdateIconUser(self.id,icon))
        except ConnectionRefusedError as e:
            print(e)
        except Exception as e:
            pass

    def SignOut(self):
        self.connect_monitor.send(SignOut())
        self.new_message.terminate()
        self.ConfigClient()
        widget.Authorization()


class MyWindow(QStackedWidget):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setGeometry(0, 0, 600, 600)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowIcon(QIcon('InterfaceData/Icon/Icon_.png'))
        self.setWindowTitle('NewMess')
        self.setMouseTracking(False)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.loginform = AuthorizationsUser(LocalClient)
        self.registerform = RegistrationWindow(LocalClient)
        self.chatform = MyChatsManager(LocalClient)
        self.currentChanged.connect(self.ClearWidget)
        self.center()

    def Start(self):
        [self.addWidget_(i) for i in (self.loginform, self.registerform, self.chatform)]

    def Roll_up(self):
        self.setWindowState(self.windowState() | Qt.WindowMinimized)

    def showScreenWindow(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()
        return self.isFullScreen()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def LaunchMyChat(self):
        self.setGeometry(0,0, 1280, 720)
        self.setCurrentIndex(self.indexOf(chatform))
        self.center()

    def Authorization(self):
        self.setGeometry(0, 0, 600, 600)
        self.setCurrentIndex(self.indexOf(loginform))
        self.center()

    def Registration(self):
        self.setGeometry(0, 0, 600, 600)
        self.setCurrentIndex(self.indexOf(registerform))
        self.center()


    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()


    def mouseMoveEvent(self, event):
        try:
            delta = QPoint(event.globalPos() - self.oldPos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPos = event.globalPos()
        except Exception:
            pass

    def addWidget_(self, w: QWidget) -> None:
        self.addWidget(w)
        w.Get_widget(self)

    def ClearWidget(self):
        self.currentWidget().ClearWidget()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    LocalClient = LocalClient()
    widget = MyWindow()
    widget.Start()
    loginform = widget.loginform
    registerform = widget.registerform
    chatform = widget.chatform
    widget.Authorization()
    widget.show()
    sys.exit(app.exec_())
