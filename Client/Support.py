from base64 import b64encode
from PyQt5.QtCore import QByteArray,QBuffer,QIODevice
from PyQt5.QtGui import QPixmap

def Icon(src):
    with open(src, "rb", ) as image:
        return b64encode(image.read())


def PixmapToBase64(Pixmap:QPixmap) -> bytes:
    ba = QByteArray()
    buff = QBuffer(ba)
    buff.open(QIODevice.WriteOnly)
    Pixmap.save(buff, "PNG")
    ImageByte = ba.toBase64().data()
    return ImageByte


class list_id(set):
    def __init__(self,*args):
        super().__init__(args)
        
    def to_list(self) -> list:
        return list(self)

    def __getitem__(self,other):
        return self.to_list()[other]
    

