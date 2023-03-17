# -*- coding: utf-8 -*-
from InterfaceData.InterfaceObject.Object import *
from InterfaceData.Painter.PaintAndMask import mask_image
from Support import Icon, PixmapToBase64
from data.Validators import PasswordValidator, EmailValidator, NameValidator, ValidationError

pasw_valid = PasswordValidator(3, 255)
email_valid = EmailValidator()
name_valid = NameValidator(2, 255)
TestName = ['from', '4', 'Join', 'Test']


class settings(QMainWindow):
    def __init__(self,mysignal=None,icon:str=None):
        super().__init__()
        self.mysignal = mysignal
        uic.loadUi('InterfaceData/ui/settings_.ui', self)
        self.setGeometry(0, 0, 600, 80)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.Exit_Settings.clicked.connect(self.Exit_)
        self.EditIconlUser_.clicked.connect(self.dialog)
        self.setIconUser(icon)

        self.Exit_Settings.setStyleSheet("""QPushButton#Exit_Settings {
                                border: 1px
                                ;}
                                QPushButton#Exit_Settings:hover {
                                background-color:#EB0400;
                                color: #fff;
                                }""")

    def setIconUser(self, img):
        ba = QByteArray.fromBase64(img)
        pixmap = QPixmap()
        if pixmap.loadFromData(ba, "PNG"):
            self.IconUser_.setPixmap(pixmap)

    def Exit_(self):
        self.hide()

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        try:
            delta = QPoint(event.globalPos() - self.oldPos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPos = event.globalPos()
        except AttributeError:
            pass

    def dialog(self):
        try:
            file, check = QFileDialog.getOpenFileName(None,
                                                      "QFileDialog.getOpenFileName()",
                                                      "",
                                                      "All Files (*);;Image Files (*.png);;Image Files (*.jpg)")

            if check:
                Icon_ = mask_image(open(file, 'rb').read(),
                                   file.rsplit('.', maxsplit=1)[-1])
                self.Image = PixmapToBase64(Icon_)
                self.IconUser_.setPixmap(Icon_)
                self.mysignal.emit(dict(form='UpdateIconUser', Icon=self.Image))
        except Exception as e:
            print(e)


class Creater_Chat_(QMainWindow):
    def __init__(self,mysignal=None):
        super().__init__()
        self.mysignal = mysignal
        self.ChatParticipantId = list()
        self.IconCustominCreateChat = QLabel
        self.CountParticipants = QLabel
        uic.loadUi('InterfaceData/ui/Creator_Chat.ui', self)
        self.IconCustominCreateChat.hide()
        self.CountParticipants.setText('0')
        self.Image = ''
        self.setGeometry(0, 0, 670, 550)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.FindButtonToCreateChat.clicked.connect(self.__Find)
        self.CreateChatButton.clicked.connect(self.__Created)
        self.Exit.clicked.connect(self.Exit_)
        self.LoadIconChat.clicked.connect(self.dialog)
        self.Exit.setStyleSheet("""QPushButton#Exit {
                                border: 1px;    
                                }
                                QPushButton#Exit:hover {
                                background-color:#EB0400;
                                color: #fff;
                                }""")

    def __Find(self):
        text = self.LineEditToCreateChat.text()
        self.mysignal.emit(dict(form='Find', SearchTarget=text))

    def Find_Handler(self, listuser: list):
        self.listWidgetCreateChat.clear()
        for id, user in listuser:
            myQCustomQWidget = QUserChat(id, self.ChatParticipantId,
                                         self.CountParticipants)
            myQCustomQWidget.setText_(user)
            myQListWidgetItem = QListWidgetItem(self.listWidgetCreateChat)
            myQListWidgetItem.setSizeHint(myQCustomQWidget.sizeHint())
            self.listWidgetCreateChat.addItem(myQListWidgetItem)
            self.listWidgetCreateChat.setItemWidget(myQListWidgetItem, myQCustomQWidget)

    def __Created(self):
        try:
            self.mysignal.emit(dict(form='CreateChat',
                                             title=self.NameChatLineEdit.text(),
                                             ListIdUsers=self.ChatParticipantId,
                                             Icon=self.Image))
            self.ChatParticipantId = list()
            self.NameChatLineEdit.clear()
            self.CountParticipants.setText('0')
            self.listWidgetCreateChat.clear()
            self.LineEditToCreateChat.clear()

            self.Exit_()
        except Exception as e:
            print(e)

    def dialog(self):
        file, check = QFileDialog.getOpenFileName(None, "QFileDialog.getOpenFileName()",
                                                  "",
                                                  "All Files (*);;Image Files (*.png);;Image Files (*.jpg)")
        if check:
            if self.IconCustominCreateChat.isHidden():
                self.IconCustominCreateChat.show()
            Icon_ = mask_image(open(file, 'rb').read(), file.rsplit('.', maxsplit=1)[-1])
            self.Image = PixmapToBase64(Icon_)
            self.IconCustominCreateChat.setPixmap(Icon_)

    def Exit_(self):
        self.hide()

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        try:
            delta = QPoint(event.globalPos() - self.oldPos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPos = event.globalPos()
        except AttributeError:
            pass


class AuthorizationsUser(QMainWindow):
    def __init__(self, mysignal):
        super().__init__()
        uic.loadUi('InterfaceData/ui/Authorization.ui', self)
        self.Error_login.hide()
        self.mysignal = mysignal
        self.Enter.clicked.connect(self.Enter_)
        self.Exit_Login.clicked.connect(self.Exit_)
        self.Roll_Up_Login.clicked.connect(self.Roll_up)
        self.Registration.clicked.connect(self.Registration_1)
        self.Exit_Login.setStyleSheet("""QPushButton#Exit_Login {
                                border: 1px
                                ;}
                                QPushButton#Exit_Login:hover {
                                background-color:#EB0400;
                                color: #fff;
                                }""")
        self.Roll_Up_Login.setStyleSheet("""QPushButton#Roll_Up_Login {
                                    border: 1px;
                                    }
                                   QPushButton#Roll_Up_Login:hover {
                                   background-color: #979797;
                                   color: #fff;
                                   }""")
        self.Registration.setStyleSheet("""
                                    QPushButton#Registration{
                                    background:#989898;
                                    border-radius:20px;
                                    }
                                   QPushButton#Registration:hover {
                                   background-color: #64b5f6;
                                   color: #fff;
                                   }""")
        self.Enter.setStyleSheet("""QPushButton#Enter{
                                    background:#989898;
                                    border-radius:20px;
                                    }
                                   QPushButton#Enter:hover {
                                   background-color: #00CA87;
                                   color: #fff;
                                   }""")

    def Enter_(self):
        try:
            name, password = self.NameLogin.text(), self.PasswordLogin.text()
            if not name: raise ValidationError('Введите имя пользователя')
            if not password: raise ValidationError('Введите пароль пользователя')
            self.mysignal.emit(dict(form='Authorizations',
                                             name=self.NameLogin.text(),
                                             password=self.PasswordLogin.text()))
        except ValidationError as e:
            self.Error_mes(*e.args)
        except Exception as e:
            print(e)

    def Registration_1(self):
        self.widget.Registration()

    def Get_Frame(self, widget):
        self.widget = widget

    def Roll_up(self):
        self.widget.Roll_up()

    def Exit_(self):
        sys.exit()

    def ClearWidget(self):
        self.NameLogin.clear()
        self.PasswordLogin.clear()

    def Error_mes(self, mes:str):
        if self.Error_login.isHidden():
            self.Error_login.show()
        self.Error_login.setText(mes)


class RegistrationWindow(QMainWindow):
    def __init__(self,mysignal):
        super().__init__()
        self.mysignal = mysignal
        self.setStyleSheet("""border-radius:0px;""")

        uic.loadUi('InterfaceData/ui/Registr.ui', self)  # Загружаем дизайн
        self.Exit_Reg.clicked.connect(self.Exit_)
        self.Register_button.clicked.connect(self.Registration_)
        self.Roll_Up_Reg.clicked.connect(self.Roll_up)
        self.Register_button.setStyleSheet("""QPushButton#Register_button {
                                           background:#989898;
                                           border-radius:20px
                                           }
                                           QPushButton#Register_button:hover {
                                           background-color:#64b5f6;
                                           color: #fff;
                                           }""")
        self.Exit_Reg.setStyleSheet("""QPushButton#Exit_Reg {
                                border: 1px
                                ;}
                                QPushButton#Exit_Reg:hover {
                                background-color:#EB0400;
                                color: #fff;
                                }""")
        self.Roll_Up_Reg.setStyleSheet("""QPushButton#Roll_Up_Reg {
                                    border: 1px;
                                    }
                                   QPushButton#Roll_Up_Reg:hover {
                                   background-color: #979797;
                                   color: #fff;
                                   }""")

    def Registration_(self):
        try:
            name, password, email, repeat = self.NameRegister.text(), \
                                            self.PasswordRegister.text(), \
                                            self.EmailRegister.text(), \
                                            self.RepeatPasswordRegister.text()
            if repeat != password:
                raise ValidationError('Пароли не совпадают')
            if not name: raise ValidationError('Введите имя')
            if not email: raise ValidationError('Введите свою почту')
            if not password: raise ValidationError('Введите пароль')
            pasw_valid(password)
            name_valid(name)
            email_valid(email)
            self.mysignal.emit(dict(form='Registration',name=self.NameRegister.text(),
                                            email=self.EmailRegister.text(),
                                             password=self.PasswordRegister.text()))

        except ValidationError as e:
            self.Error_mes(*e.args)


    def Get_Frame(self, widget):
        self.widget = widget


    def Roll_up(self):
        self.widget.Roll_up()


    def Exit_(self):
        sys.exit()


    def ClearWidget(self):
        self.NameRegister.clear()
        self.EmailRegister.clear()
        self.PasswordRegister.clear()
        self.RepeatPasswordRegister.clear()


    def Error_mes(self, mes):
        try:
            self.Error_reg.setText(mes)
        except Exception as e:
            print(e)


class MyChatsManager(QMainWindow):
    def __init__(self, mysignal):
        super().__init__()
        self.mysignal = mysignal
        self.Id_chat = 0
        self.chats = []
        self.Chat = QListWidget()
        self.TitleBar = QWidget
        uic.loadUi('InterfaceData/ui/ChatsManager.ui', self)
        self.font = QFont('Helvetica', 12)
        self.pix = ""
        self.NormScreenIcon = QIcon(
            QPixmap('InterfaceData/Image/window_restore_icon.svg'))
        self.FullScreenIcon = QIcon(
            QPixmap('InterfaceData/Image/window_maximize_icon.svg'))
        self.Chat.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        # self.widget.verticalScrollBar().setSingleStep(1)
        self.Chat.setFont(self.font)
        # self.Find.setPlaceholderText('Поиск')
        self.Exit.clicked.connect(self.ExitWindow)
        self.Roll_Up.clicked.connect(self.Roll_up)
        self.Send.clicked.connect(self.Send_)
        self.SignOutButton.clicked.connect(self.SignOut)
        self.Add_Chat.clicked.connect(self.Creater_Chat)
        self.showScreen_.clicked.connect(self.showScreen)
        self.ChatsMenu.itemClicked.connect(self.OpenChat)
        self.Settings.clicked.connect(self.SettingsStart)
        self.Add_Chat.setIconSize(QSize(45, 45))
        self.FieldForWritingMessage.hide()
        scroll_chat_bar = CustomChatScrollBar()
        scroll_menu_chats_bar = CustomMenuChatsScrollBar()
        # setting vertical scroll bar to it
        self.Chat.setVerticalScrollBar(scroll_chat_bar)
        self.ChatsMenu.setVerticalScrollBar(scroll_menu_chats_bar)
        self.Settings.setStyleSheet("""QPushButton#Settings {
                                            border:none;
                                            border-radius:10px;
                                            color:white;
                                            }
                                            QPushButton#Settings:hover {
                                            background:#64b5f6;
                                            }""")
        self.SignOutButton.setStyleSheet("""QPushButton#SignOutButton {
                                        border: 1px;
                                        border-radius:10px;
                                        ;}
                                        QPushButton#SignOutButton:hover {
                                        color:white;
                                        background-color:#EB0400;
                                        color: #fff;
                                        }""")
        self.Exit.setStyleSheet("""QPushButton#Exit {
                                border: 1px
                                ;}
                                QPushButton#Exit:hover {
                                background-color:#EB0400;
                                color: #fff;
                                }""")
        self.Roll_Up.setStyleSheet("""QPushButton#Roll_Up {
                                    border: 1px;
                                    }
                                   QPushButton#Roll_Up:hover {
                                   background-color: #979797;
                                   color: #fff;
                                   }""")
        self.showScreen_.setStyleSheet("""QPushButton#showScreen_ {
                                            border: 1px;
                                            }
                                           QPushButton#showScreen_:hover {
                                           background-color: #979797;
                                           color: #fff;
                                           }""")

        self.Send.setStyleSheet('QPushButton#Send {'
                                'background:#D9D9D9;'
                                'border-top-left-radius: 12px;'
                                'border-bottom-left-radius: 12px;'
                                'font: 12pt "Helvetica";}'

                                'QPushButton#Send:hover'
                                ' {background:#64b5f6;}')

        self.Add_Chat.setStyleSheet("""QPushButton#Add_Chat {
                                    border:none;
                                    border-radius:10px;
                                    color:white;
                                    }
                                    QPushButton#Add_Chat:hover {
                                    background:#64b5f6;
                                    }""")

        self.textEdit.setStyleSheet('QTextEdit#textEdit {'
                                    'background:#EDEDED;'
                                    'color:black;'
                                    'border-left:1px solid #E1E1E1;}')
        self.Chat.setSpacing(8)
        self.ChatsMenu.setSpacing(0)

    def TestChat(self):
        self.Icon_ = 'C:/Users/Kanl222/PycharmProjects/PyQtProject/test/23.png'
        for index, name, icon, user in [
            ('No.2',
             "Дорогие друзья, постоянный количественный рост и сфера нашей активности обеспечивает"
             " широкому кругу специалистов участие в формировании всесторонне сбалансированных нововведений."
             " Значимость этих проблем настолько очевидна, что постоянный количественный рост и сфера нашей активности"
             " обеспечивает актуальность всесторонне сбалансированных нововведений. С другой стороны рамки и место обучения"
             " кадров обеспечивает широкому кругу специалистов участие в формировании соответствующих условий активизации?Дорогие друзья,"
             " постоянное информационно-техническое обеспечение нашей деятельности напрямую зависит от соответствующих условий активизации."
             "Разнообразный и богатый опыт реализация намеченного плана развития играет важную роль в формировании модели развития? Разнообразный"
             " и богатый опыт повышение уровня гражданского сознания представляет собой интересный эксперимент проверки новых предложений? Соображения"
             " высшего порядка, а также повышение уровня гражданского сознания способствует повышению актуальности новых предложений!Не следует, однако"
             ", забывать о том, что новая модель организационной деятельности играет важную роль в формировании соответствующих условий активизации. Соображения"
             " высшего порядка, а также сложившаяся структура организации создаёт предпосылки качественно новых шагов для дальнейших направлений развитая системы"
             " массового участия? Равным образом рамки и место обучения кадров требует определения и уточнения соответствующих условий активизации. Задача организации,"
             " в особенности же реализация намеченного плана развития требует от нас анализа системы масштабного изменения ряда параметров. Дорогие друзья, сложившаяся"
             " структура организации представляет собой интересный эксперимент проверки системы обучения кадров, соответствующей насущным потребностям?",
             'C:/Users/Kanl222/PycharmProjects/PyQtProject/test/23.png', True),
            ('1', 'Nyaruko', 'C:/Users/Kanl222/PycharmProjects/PyQtProject/test/23.png',
             False)]:
            # Create QCustomQWidget
            myQCustomQWidget = QCustomQWidgetMessage(user=user)
            myQCustomQWidget.setTextUp(index)
            myQCustomQWidget.setTextDown(name)
            myQCustomQWidget.setIcon(Icon(self.Icon_))
            self.name = '1'
            # Create QListWidgetItem
            myQListWidgetItem = QListWidgetItem(self.Chat)
            # Set size hint
            myQListWidgetItem.setSizeHint(myQCustomQWidget.sizeHint())
            # Add QListWidgetItem into QListWidget
            self.Chat.addItem(myQListWidgetItem)
            self.Chat.setItemWidget(myQListWidgetItem, myQCustomQWidget)
        self.set_single_step()

    def OpenChat(self, item: QListWidgetItem):
        self.Id_chat = int(item.text())
        try:
            if self.FieldForWritingMessage.isHidden():
                self.FieldForWritingMessage.show()
            else:
                self.textEdit.clear()
                self.Chat.clear()
            self.NameChat.setText(
            [i for i in self.chats if i[0] == self.Id_chat][0][1])
            if self.message_chats != {}:
                for message in self.mysignal.message_chats[self.Id_chat]:
                    if message[2] != self.id:
                        _, username, icon = self.mysignal.users[message[2]][0]
                        self.Add_message(username, message[3], icon)
                    else:
                        self.Add_message(self.username, message[3], self.icon)
            self.set_single_step()
        except IndexError:
            pass
        except Exception as e:
            print(e)

    def set_single_step(self):
        self.Chat.verticalScrollBar().setSingleStep(12)

    def Update_config(self, id, username, email, icon):
        self.id = id
        self.username = username
        self.email = email
        self.icon = icon

        self.sittings_window = settings(mysignal=self.mysignal,icon=icon)
        self.CreateChat = Creater_Chat_(self.mysignal)

    def showScreen(self):
        try:
            self.widget.showScreenWindow()
        except Exception as e:
            print(e)

    def SettingsStart(self):
        self.sittings_window.show()

    def LoadChats(self):
        [self.Add_Chat_In_Menu(*i) for i in self.chats]


    @pyqtSlot(int,str,str)
    def Add_Chat_In_Menu(self, id, title, icon):
        myQCustomQWidget = QChat()
        myQCustomQWidget.setTextUp(title)
        myQCustomQWidget.setIcon(icon)
        myQListWidgetItem = QListWidgetItem(self.ChatsMenu)
        myQListWidgetItem.setText(str(id))
        myQListWidgetItem.setSizeHint(myQCustomQWidget.sizeHint())
        self.ChatsMenu.addItem(myQListWidgetItem)
        self.ChatsMenu.setItemWidget(myQListWidgetItem, myQCustomQWidget)

        self.ChatsMenu.verticalScrollBar().setSingleStep(7)

    def Send_(self):
        try:
            if self.textEdit.toPlainText():
                message = self.textEdit.toPlainText()
                self.mysignal.emit(dict(form='Message', id_chat=self.Id_chat,
                                                 message=message))
        except Exception as e:
            print(e)
            
    def import_icon_chat(self,id):
        with open(src, "rb", ) as image:
            return base64.b64encode(image.read())
        
    def import_icon_user(self,id):
        with open(src, "rb", ) as image:
            return base64.b64encode(image.read())

    def Get_Frame(self, widget):
        self.widget = widget

    def Creater_Chat(self):
        self.CreateChat.show()

    def ExitWindow(self):
        sys.exit()

    def Roll_up(self):
        self.widget.Roll_up()

    def setIconUser(self, img):
        ba = QByteArray.fromBase64(img)
        pixmap = QPixmap()
        if pixmap.loadFromData(ba, "PNG"):
            self.Icon.setPixmap(pixmap)

    def ClearWidget(self):
        self.Chat.clear()
        self.ChatsMenu.clear()

    def SignOut(self):
        self.mysignal.SignOut()

    @pyqtSlot()
    def Add_message(self, user, message, icon, testflag=False):
        myQCustomQWidget = QCustomQWidgetMessage(user=(self.username == user or testflag))
        myQCustomQWidget.setTextUp(user)
        myQCustomQWidget.setTextDown(message)
        myQCustomQWidget.setIcon(icon)
        myQListWidgetItem = QListWidgetItem(self.Chat)
        myQListWidgetItem.setSizeHint(myQCustomQWidget.sizeHint())
        self.Chat.addItem(myQListWidgetItem)
        self.Chat.setItemWidget(myQListWidgetItem, myQCustomQWidget)
        self.Chat.scrollToBottom()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    loginform = AuthorizationsUser(1)
    registerform = RegistrationWindow(1)
    chatform = MyChatsManager(1)
    h = Creater_Chat_()
    chatform.setGeometry(0, 0, 1280, 720)
    # chatform.showFullScreen()
    print(chatform.size())
    chatform.show()
    sys.exit(app.exec_())
