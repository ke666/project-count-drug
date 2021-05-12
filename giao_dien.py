from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import QTimer,QByteArray, QDir
import  sys
import cv2
import numpy as np
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
    count = 0
    # class constructor
    def __init__(self, parent=None):
        # call QWidget constructor
        super(Do_an, self).__init__(parent=parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.image = QImage()
        self.image2 = QImage()
        # create a timer
        self.timer = QTimer()
        # set timer timeout callback function
        self.timer.timeout.connect(self.viewCam)
        #self.ui.pushButton.clicked.connect(self.additem)
        self.ui.pushButton_2.clicked.connect(self.start)
        self.ui.lineEdit.returnPressed.connect(self.additem)
        self.ui.lineEdit.returnPressed.connect(self.Savee)
        self.ui.lineEdit.returnPressed.connect(self.puttext)
        self.ui.pushButton.clicked.connect(self.controlTimer)
        self.ui.pushButton_3.clicked.connect(self.Savee)
    def start(self) :
        self.image = Do_an.L[0]
        self.displayImage_3()
        self.image2 = Do_an.im
        self.displayImage_2()
        self.ui.lineEdit_2.setText(str(len(Do_an.L)))
    def additem(self):
        # self.ui.lineEdit.text()
        if not self.ui.lineEdit.text()=="":
            self.ui.listWidget.addItem(str(Do_an.count + 1) + '.' + self.ui.lineEdit.text())
            self.stt = self.ui.lineEdit.text()
            self.ui.lineEdit.setText("")
            self.loadImage(Do_an.L)
            Do_an.count += 1
    def puttext(self):
        (x, y, w, h) = cv2.boundingRect(Do_an.cntss[Do_an.count])
        xm = x + int (w/2)
        ym = y + int (h/2)
        cv2.putText(self.image2, str(self.stt), (xm, ym), cv2.FONT_HERSHEY_SIMPLEX, 1, (200, 255, 155), 2, cv2.LINE_AA)
        self.displayImage_2()
    def loadImage(self,list):
        self.image = list[Do_an.count]
            # self.image = cv2.imread(k)
        self.displayImage_3()
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
    def Savee(self):
        cv2.imwrite('images/'+str(self.stt) +".png",self.image)

    def viewCam(self):
        # read image in BGR format
        ret, image = self.cap.read()
        # convert image to RGB format
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
            # create video capture
            self.cap = cv2.VideoCapture(0)
            # start timer
            self.timer.start(20)
            # update control_bt text
            self.ui.pushButton.setText("Dừng")
        # if timer is started
        else:
            # stop timer
            self.timer.stop()
            # release video capture
            self.cap.release()
            # update control_bt text
            self.ui.pushButton.setText("Chạy")

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#
#     # create and show mainWindow
#     doan = Do_an()
#     doan.show()
#
#     sys.exit(app.exec_())