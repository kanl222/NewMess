import os
import sys
from base64 import b64decode
from PyQt5.QtWidgets import QWidget,QApplication, QPushButton, QSlider, QVBoxLayout, \
    QHBoxLayout, QListWidget, QListWidgetItem, QGroupBox, QDialog, QFrame, \
    QSizePolicy
from PyQt5.QtWidgets import QLabel, QLineEdit, QGridLayout, QMainWindow, QDesktopWidget, \
    QSpacerItem, QLayout, QFileDialog, QAbstractItemView, QScrollBar
from PyQt5.QtGui import  QPixmap, QFont, QIcon,QImage,QRegExpValidator
from PyQt5.QtCore import QPointF, Qt, QRect, QPoint, QEvent, pyqtSlot, QByteArray, QSize, \
    QAbstractItemModel,QRegExp
from PyQt5 import uic
from textwrap import wrap


class Message(QGroupBox):
    def __init__(self, parent=None, user=False):
        QWidget.__init__(self, parent=parent)
        self.textQVBoxLayout = QVBoxLayout()
        self.font_up = QFont('Helvetica', 10)
        self.font_down = QFont('Helvetica', 10)
        self.textQVBoxLayout.setSizeConstraint(QLayout.SizeConstraint.SetMinimumSize)
        self.textUpQLabel = QLabel()
        self.textDownQLabel = QLabel()
        self.textUpQLabel.setFont(self.font_up)
        self.textDownQLabel.setFont(self.font_down)
        self.textQVBoxLayout.addWidget(self.textUpQLabel)
        self.textQVBoxLayout.addWidget(self.textDownQLabel)
        self.setLayout(self.textQVBoxLayout)
        # setStyleSheet
        if user:
            self.textDownQLabel.setAlignment(Qt.AlignLeft)
            self.textUpQLabel.setAlignment(Qt.AlignRight)
            self.textQVBoxLayout.setAlignment(Qt.AlignRight)
            self.setStyleSheet(f"""
                        background:#00CA87;
                        border:none;
                        border-radius:16px;
                        padding-right: 2px;

                        """)
        else:
            self.setStyleSheet(f"""
                        background:#A4A4A4;
                        border:none;
                        border-radius:16px;
                        margin-left: 2px;
                        """)


class QCustomQWidgetMessage(QWidget):
    def __init__(self, parent=None, user=False):
        super(QCustomQWidgetMessage, self).__init__(parent)
        self.container = Message(self, user)
        self.spacer = QSpacerItem(320, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.allQHBoxLayout = QHBoxLayout()
        self.iconQLabel = QLabel()
        self.iconQLabel.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        self.allQHBoxLayout.setSizeConstraint(QLayout.SizeConstraint.SetMinimumSize)
        if user:
            self.allQHBoxLayout.addItem(self.spacer)
            self.allQHBoxLayout.addWidget(self.container, 1)
            self.allQHBoxLayout.addWidget(self.iconQLabel, 0)
        else:
            self.allQHBoxLayout.addWidget(self.iconQLabel, 0)
            self.allQHBoxLayout.addWidget(self.container, 1)
            self.allQHBoxLayout.addItem(self.spacer)
        self.setLayout(self.allQHBoxLayout)
        # setStyleSheet
        self.iconQLabel.setStyleSheet("""
                background:#212226;
                width-max:45pxl;height-max:45;
        """)
        self.container.textUpQLabel.setStyleSheet('''
                    color: black;
                ''')
        self.container.textDownQLabel.setStyleSheet('''
                    color: black;
                ''')

    def setTextUp(self, text):
        self.container.textUpQLabel.setText(text)

    def setTextDown(self, text):
        if len(text) * 8 < 320:
            self.container.setMaximumWidth(len(text) * 8)
            self.container.textDownQLabel.setText(text)
        else:
            self.container.setMaximumWidth(320)
            wrapped_s = '\n'.join(wrap(text, width=40))
            self.container.textDownQLabel.setText(wrapped_s)

    def setIcon(self, image):
        ba = QByteArray.fromBase64(image)
        pixmap = QPixmap()
        if pixmap.loadFromData(ba, "PNG"):
            self.iconQLabel.setPixmap(pixmap)


class QMessage(QGroupBox):
    def __init__(self, parent=None, user=False):
        super().__init__(parent)
        self.setStyleSheet("""border:none""")
        self.font_up = QFont('Helvetica', 12)
        self.font_down = QFont('Helvetica', 12)
        self.textQVBoxLayout = QVBoxLayout()
        self.textUpQLabel = QLabel()
        self.textDownQLabel = QLabel()
        self.textUpQLabel.setFont(self.font_up)
        self.textDownQLabel.setFont(self.font_down)
        self.textDownQLabel.setWordWrap(True)
        self.textQVBoxLayout.addWidget(self.textUpQLabel)
        self.textQVBoxLayout.addWidget(self.textDownQLabel)
        self.iconQLabel = QLabel()
        self.setLayout(self.textQVBoxLayout)
        # setStyleSheet

        if user:
            self.setStyleSheet(f"""
            background:#00CA87;
            border:none;
            border-radius:10px;
            """)
            self.textDownQLabel.setAlignment(Qt.AlignRight)
            self.textUpQLabel.setAlignment(Qt.AlignRight)
            self.textQVBoxLayout.setAlignment(Qt.AlignRight)
        else:
            self.setStyleSheet(f"""
            background:#A4A4A4;
            border:none;
            border-radius:10px;
            """)
        self.textUpQLabel.setStyleSheet('''
            color: black;
        ''')
        self.textDownQLabel.setStyleSheet('''
            color: black;
        ''')

    def setTextUp(self, text):
        self.textUpQLabel.setText(text)

    def setTextDown(self, text):
        self.textDownQLabel.setText(text)


class QUserChat(QGroupBox):
    def __init__(self, id, list_:list,count, parent=None):
        super().__init__(parent)
        self.font_up = QFont('Helvetica', 14)
        self.textQHBoxLayout = QHBoxLayout()
        self.textLabel = QLabel(self)
        self.labelcount = count
        self.Button = QPushButton(self)
        self.Button.clicked.connect(lambda: self.AddParticipants(id,list_,count))
        self.Button.setIcon(QIcon('InterfaceData/Image/plus.svg'))
        self.Button.setIconSize(QSize(32,32))
        self.Button.setMaximumSize(32,32)
        self.Button.setMinimumSize(32, 32)
        self.textLabel.setFont(self.font_up)
        self.textQHBoxLayout.addWidget(self.textLabel, 1)
        self.textQHBoxLayout.addWidget(self.Button, 0)
        self.setLayout(self.textQHBoxLayout)

        # setStyleSheet

        self.textLabel.setStyleSheet('''
            color: black;
        ''')
        self.Button.setStyleSheet("""
        """)

    def setText_(self, text):
        self.textLabel.setText(text)

    def AddParticipants(self,id,list_,count):
        if not id in list_:
            list_.append(id), count.setText(f"{len(list_)}")

    def setFunctionButton(self, command):
        self.Button.clicked.connect(command)


class InfChat(QGroupBox):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)
        self.font_up = QFont('Helvetica', 8)
        self.textQVBoxLayout = QVBoxLayout()
        self.setLayout(self.textQVBoxLayout)
        self.textUpQLabel = QLabel()
        self.textDownQLabel = QLabel()
        self.textUpQLabel.setFont(self.font_up)
        self.textQVBoxLayout.addWidget(self.textUpQLabel)
        self.textQVBoxLayout.addWidget(self.textDownQLabel)


class QChat(QGroupBox):
    def __init__(self, id=0, parent=None):
        super().__init__(parent)
        self.id = id
        self.container = InfChat(self)
        self.iconQLabel = QLabel()
        self.allQHBoxLayout = QHBoxLayout()
        self.allQHBoxLayout.addWidget(self.iconQLabel, 0)
        self.allQHBoxLayout.addWidget(self.container, 1)
        self.allQHBoxLayout.setSpacing(6)
        self.setLayout(self.allQHBoxLayout)
        # setStyleSheet
        self.setStyleSheet("""
            border:none;
            border-bottom: 2px solid grey;
        """)
        self.container.setStyleSheet('''
            border:none;
            color: black;
        ''')
        self.iconQLabel.setStyleSheet('''
                    border:none;
                ''')

    def setTextUp(self, text):
        self.container.textUpQLabel.setText(text)

    def setTextDown(self, text):
        if len(text) >= 24:
            self.container.textDownQLabel.setText(f"{text[:24]}...")
        else:
            self.container.textDownQLabel.setText(text)

    def setIcon(self, image):
        if image is not None:
            try:
                ba = QByteArray.fromBase64(image)
                pixmap = QPixmap()
                if pixmap.loadFromData(ba, "PNG"):
                    self.iconQLabel.setPixmap(pixmap)
            except Exception as e:
                print(e)


class CustomChatScrollBar(QScrollBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
                QWidget {
                    background-color: #212226;
                }
                /* VERTICAL SCROLLBAR */
                QScrollBar:vertical {
                    border: none;
                    background: rgb(33, 34, 38,0.1);
                    width: 14px;
                    margin: 1px 0 1px 0;
                    border-radius: 0px;
                }
                
                /*  HANDLE BAR VERTICAL */
                QScrollBar::handle:vertical {
                    background-color: rgba(129, 132, 145,0.4);
                    min-height: 30px;
                    border-radius: 7px;
                }
                
                QScrollBar::add-line:vertical {
                    height: 0px;
                    subcontrol-position: bottom;
                    subcontrol-origin: margin;
                }
                QScrollBar::sub-line:vertical {
                    height: 0 px;
                    subcontrol-position: top;
                    subcontrol-origin: margin;
                    }
                /* RESET ARROW */
                QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
                    background: none;
                }
                QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                    background: none;
                }
            """)


class CustomMenuChatsScrollBar(QScrollBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
                QWidget {
                    background: rgba(0,0,0,0.5);
                }
                /* VERTICAL SCROLLBAR */
                QScrollBar:vertical {
                    border: none;
                    background: white;
                    width: 10px;
                    margin: 1px 1px 1px 1px;
                    border-radius: 0px;
                }

                /*  HANDLE BAR VERTICAL */
                QScrollBar::handle:vertical {
                    background-color: rgba(129, 132, 145,0.4);
                    min-height: 30px;
                    border-radius: 4px;
                }

                QScrollBar::add-line:vertical {
                    height: 0px;
                    subcontrol-position: bottom;
                    subcontrol-origin: margin;
                }
                QScrollBar::sub-line:vertical {
                    height: 0 px;
                    subcontrol-position: top;
                    subcontrol-origin: margin;
                    }
                /* RESET ARROW */
                QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
                    background: none;
                }
                QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                    background: none;
                }
            """)
