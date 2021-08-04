####file main
import Detect as De
import cv2
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from giao_dien import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import QTimer,QByteArray, QDir
from PyQt5.QtCore import QDir, Qt, QUrl
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import (QApplication, QFileDialog, QHBoxLayout, QLabel,
        QPushButton, QSizePolicy, QSlider, QStyle, QVBoxLayout, QWidget)



#get frame from video
inputvideo = cv2.VideoCapture(0)
# inputvideo = cv2.VideoCapture('http://192.168.1.103:8080/video')
    success, image =  inputvideo.read()
    count = 0
    success = True
    while success:
    # cv2.imwrite("frame%d.jpg" % count, image)
        cv2.imwrite("frame20.jpg" ,image)
        success, image = inputvideo.read()
        print('read a new frame:', success)
        count += 1
        if count > 10:
            break


imgg,L,tuplee = De.Crush("frame20.jpg")
Do_an.Getlist(Do_an,imgg,L,tuplee)
app = QApplication(sys.argv)

# create and show mainWindow
doan = Do_an()
doan.show()

sys.exit(app.exec_())