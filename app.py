# from _typeshed import Self
from imutils import contours
import numpy as np
import imutils
import Detect as De
import cv2
from os import name
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import QTimer,QByteArray, QDir
from PyQt5.QtCore import QDir, Qt, QUrl
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import (QApplication, QFileDialog, QHBoxLayout, QLabel,
        QPushButton, QSizePolicy, QSlider, QStyle, QVBoxLayout, QWidget)
import  sys
from giao_dien_rc import  *
# import Detect as De
# L = De.Crush('pic1.jpg')

class Do_an(QMainWindow):
    L = []
    cntss = ()
    im = np.array([])
    def Getlist(self,im,listt,tup):
        Do_an.L = listt
        Do_an.im = im
        Do_an.cntss = tup
    # class constructor
    def __init__(self, parent=None):
        # call QWidget constructor
        super(Do_an, self).__init__(parent=parent)
        self.ui = Ui_MainWindow() #lay từ file giao_dien_rc
        self.ui.setupUi(self)
        self.image = QImage()
        self.image2 = QImage()
        # create a timer
        self.timer = QTimer()
        # set timer timeout callback function
        self.timer.timeout.connect(self.viewCam)
        self.ui.pushButton_2.clicked.connect(self.start)
        self.ui.lineEdit.returnPressed.connect(self.labelFieldEntered)
        self.ui.pushButton.clicked.connect(self.openClicked)
        self.ui.pushButton_4.clicked.connect(self.controlTimer)

    def labelFieldEntered(self):
        if self.ui.lineEdit.text()=="": return
        if Do_an.count >= len(Do_an.L): return

        self.stt = self.ui.lineEdit.text()
        cv2.imwrite("images/"+str(self.stt)+".png",self.image)

        self.ui.listWidget.addItem(str(Do_an.count+1) + '.' + self.ui.lineEdit.text())
        self.puttext()

        Do_an.count += 1
        if Do_an.count < len(Do_an.L):
            self.image = Do_an.L[Do_an.count]
            self.displayImage_3()
            self.ui.lineEdit.setText("")
        else:
            self.ui.lineEdit.setEnabled(False)
            self.ui.label_3.setPixmap(QPixmap())


    def openClicked(self):
        filename = QFileDialog.getOpenFileName()
        self.path = filename[0]
        self.ui.input_link.setText(self.path)                        
        self.inputvideo = cv2.VideoCapture(filename[0])
        self.ui.pushButton_4.setEnabled(True)  
        self.ui.pushButton_3.setEnabled(True) 
        self.ui.pushButton_2.setEnabled(True)     
        return filename[0]
    
    def start(self) :
        Do_an.count = 0 
        inputvideo = cv2.VideoCapture(self.path)
        for i in range(10):                
            success, image = inputvideo.read()
            # imgg,L,tuplee = De.Crush("frame.jpg")
        imgg,L,tuplee = De.Crush(image)
        Do_an.Getlist(Do_an,imgg,L,tuplee)

        inputvideo.release()               
        self.image = Do_an.L[0]
        self.displayImage_3()
        self.image2 = Do_an.im
        self.displayImage_2()
        self.ui.lineEdit_2.setText(str(len(Do_an.L)))

    def puttext(self):
        (x, y, w, h) = cv2.boundingRect(Do_an.cntss[Do_an.count])
        xm = x 
        ym = y         
        cv2.putText(self.image2, str(self.stt), (xm, ym), cv2.FONT_HERSHEY_SIMPLEX, 1, (200, 255, 155), 2, cv2.LINE_AA)
        self.displayImage_2()

    

    def displayImage_2(self):
        qformat = QImage.Format_RBG32qformat = QImage.Format_Indexed8
        if len(self.image2.shape) == 3:
            if self.image2.shape[2] == 4:
                qformat = QImage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB888
        img = QtGui.QImage(self.image2.data, self.image2.shape[1], self.image2.shape[0], self.image2.strides[0], qformat)
        img = img.rgbSwapped()
        self.ui.label_2.setPixmap(QPixmap.fromImage(img))
        self.ui.label_2.setAlignment(QtCore.Qt.AlignCenter)

    def displayImage_3(self):
        qformat = QImage.Format_RBG32qformat = QImage.Format_Indexed8
        if len(self.image.shape) == 3:
            if self.image.shape[2] == 4:
                qformat = QImage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB888
        img = QtGui.QImage(self.image.data, self.image.shape[1], self.image.shape[0], self.image.strides[0], qformat)
        img = img.rgbSwapped()
        self.ui.label_3.setPixmap(QPixmap.fromImage(img))
        self.ui.label_3.setAlignment(QtCore.Qt.AlignCenter)
        
    # def Savee(self):
    #     cv2.imwrite("images/"+str(self.stt)+".png",self.image) 

    def viewCam(self):
        # read image in BGR format
        
        # convert image to RGB format        
        ret, image =  self.inputvideo.read() 
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)        
        # get image infos
        height, width, channel = image.shape
        step = channel * width
        # create QImage from image
        qImg = QImage(image.data, width, height, step, QImage.Format_RGB888)
        # show image in img_label
        self.ui.label.setPixmap(QPixmap.fromImage(qImg))
        ####start/stop timer    
    
    def controlTimer(self):
        # if timer is stopped
        if not self.timer.isActive():
            self.inputvideo = cv2.VideoCapture(self.path)  
            self.timer.start(20) # start timer
            # update control_bt text
            self.ui.pushButton_4.setText("Dừng")
            # if timer is started
        else:            
            # stop timer
            self.timer.stop()
            # release video capture
            self.inputvideo.release()
            # update control_bt text
            self.ui.pushButton_4.setText("Chạy")
            
if __name__ == '__main__':
    import sys    
    app = QApplication(sys.argv)
    doan = Do_an()
    doan.show()

    sys.exit(app.exec_())     