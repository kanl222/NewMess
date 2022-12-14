from PyQt5.QtGui import QPainter,QPixmap, QBrush,QImage,QColor,QFont,qRgb
from PyQt5.QtCore import Qt, QRect,QSize,QRectF
from numpy import random



def mask_image(imgdata, imgtype='png', size=45) -> QPixmap:
    image = QImage.fromData(imgdata, imgtype)
    image.convertToFormat(QImage.Format_ARGB32)
    imgsize = min(image.width(), image.height())
    rect = QRect(
        (image.width() - imgsize) // 2,
        (image.height() - imgsize) // 2,
        imgsize,
        imgsize,
    )
    image = image.copy(rect)
    out_img = QImage(imgsize, imgsize, QImage.Format_ARGB32)
    out_img.fill(Qt.transparent)
    painter = QPainter(out_img)
    painter.setBrush(QBrush(image))
    painter.setPen(Qt.NoPen)
    painter.drawEllipse(0, 0, imgsize, imgsize)
    painter.end()
    pm = QPixmap.fromImage(out_img)
    pm = pm.scaled(size, size, Qt.KeepAspectRatio,
                   Qt.SmoothTransformation)
    return pm

def CtreateAvatar(text:str) -> QPixmap:
    text = ''.join([i[0].upper() for i in text.split(' ')])
    imgsize = 256
    size = QSize(45,45)
    out_img = QImage(imgsize, imgsize, QImage.Format_ARGB32)
    brush = QBrush(out_img)
    font = QFont("Roboto")
    font.setPointSize(112)
    brush.setColor(Qt.white)
    painter = QPainter(out_img)
    painter.setPen(Qt.NoPen)
    painter.setBrush(QBrush(QColor(qRgb(*tuple(random.random(size=3) * 200)))))
    painter.drawEllipse(0, 0, imgsize-1, imgsize-1)
    painter.setFont(font)
    painter.setPen(Qt.white)
    painter.drawText(QRectF(0.0,0.0,imgsize,imgsize), Qt.AlignCenter, text)
    painter.end()
    pm = QPixmap.fromImage(out_img)
    pm = pm.scaled(size, Qt.KeepAspectRatio,Qt.SmoothTransformation)
    return pm