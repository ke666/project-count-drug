from imutils import contours
import numpy as np
import imutils
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
    count = 0
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
        self.ui.lineEdit.returnPressed.connect(self.additem)
        self.ui.lineEdit.returnPressed.connect(self.Savee)
        self.ui.lineEdit.returnPressed.connect(self.puttext)
        self.ui.pushButton.clicked.connect(self.openClicked)
        self.ui.pushButton_4.clicked.connect(self.controlTimer)      
        self.ui.pushButton_3.clicked.connect(self.Savee)

    # def openFile(self):
    #     fileName, _ = QFileDialog.getOpenFileName(self, "Open Movie",
    #             QDir.homePath())

    #     if fileName != '':
    #         self.mediaPlayer.setMedia(
    #                 QMediaContent(QUrl.fromLocalFile(fileName)))
    #         #self.playButton.setEnabled(True)

    
    def start(self) :
        # inputvideo = cv2.VideoCapture()
        # for i in range(10):                
        #     success, image = inputvideo.read()
        #     cv2.imwrite("frame.jpg" ,image)
        #     print('read a new frame:', success) 
        self.image = Do_an.L[0]
        self.displayImage_3()
        self.image2 = Do_an.im
        self.displayImage_2()
        self.ui.lineEdit_2.setText(str(len(Do_an.L)))
        # inputvideo = cv2.VideoCapture()
        # for i in range(50):                
        #     success, image = inputvideo.read()
        #     cv2.imwrite("frame.jpg" ,image)
        #     print('read a new frame:', success) 
        #get frame from video

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
    
    def openClicked(self):
        filename = QFileDialog.getOpenFileName()
        self.path = filename[0]
        self.ui.input_link.setText(self.path)                        
        self.inputvideo = cv2.VideoCapture(filename[0])        
        return filename[0]

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

             
         
    

    
        
# #===================================================================
# def Crush(image) :
#     img = cv2.imread(image)
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     gray = cv2.GaussianBlur(gray, (9, 9), 0)
#     edged = cv2.Canny(gray, 50, 100)
#     edged = cv2.dilate(edged, None, iterations=1)
#     edged = cv2.erode(edged, None, iterations=1)
#     # find contours in the edge map
#     cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#     cnts = imutils.grab_contours(cnts)
#     # sort the contours from left-to-right and initialize the
#     (cnts, _) = contours.sort_contours(cnts)
#     m = list(np.arange(len(cnts)))
#     print(m)
#     m_copy = m.copy()
#     n = []
#     listOI = []
#     m3 = 0
#     for c in m:
#         if c in n:
#             continue
#         if cv2.contourArea(cnts[c]) < 100:
#             if c in m_copy:
#                 m_copy.remove(c)
#             continue
#         mask_c = np.zeros(gray.shape, dtype="uint8")
#         cv2.drawContours(mask_c, cnts, c, (255, 255, 255), -1)
#         img_c = cv2.bitwise_and(img, img, mask=mask_c)
#         for j in m:
#             if (j is c) or (j in n):
#                 continue
#             if cv2.contourArea(cnts[j]) < 100:
#                 if j in m_copy:
#                     m_copy.remove(j)
#                 continue
#             mask = np.zeros(gray.shape, dtype="uint8")
#             cv2.drawContours(mask, cnts, j, 255, -1)
#             (x, y, w, h) = cv2.boundingRect(cnts[j])
#             imageROI = img[y:y + h, x:x + w]
#             maskROI = mask[y:y + h, x:x + w]
#             imageROI = cv2.bitwise_and(imageROI, imageROI, mask=maskROI)
#             # compare imageROI_c  vs rotated
#             for angle in np.arange(0, 360, 10):
#                 template = imutils.rotate_bound(imageROI, angle)
#                 # cv2.imshow('1', template)
#                 # cv2.imshow('2', img_c)
#                 # cv2.waitKey(100)
#                 template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
#                 img_gray = cv2.cvtColor(img_c, cv2.COLOR_BGR2GRAY)
#                 res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
#                 threshold = 0.9
#                 loc = np.where(res >= threshold)
#                 # Remove object
#                 k = np.array(loc)
#                 m1 = k.shape
#                 if m1 != (2, 0):
#                     n.append(j)
#                     if j in m_copy:
#                         m_copy.remove(j)
#                     break
#     for a in n:
#         for b in n:
#             if b == a:
#                 n.remove(b)
#     mask_orig = np.zeros(gray.shape, dtype="uint8")
#     for k in m_copy:
#         cv2.drawContours(mask_orig, cnts, k, (255, 255, 255), -1)
#     img_orig = cv2.bitwise_and(img, img, mask=mask_orig)
#     for i in m_copy :
#         mask_orig = np.zeros(gray.shape, dtype="uint8")
#         cv2.drawContours(mask_orig, cnts, i, 255, -1)
#         (x2, y2, w2, h2) = cv2.boundingRect(cnts[i])
#         imageROI_orig = img[y2:y2 + h2, x2:x2 + w2]
#         maskROI_orig = mask_orig[y2:y2 + h2, x2:x2 + w2]
#         imageROI_orig = cv2.bitwise_and(imageROI_orig, imageROI_orig, mask=maskROI_orig)
#         listOI.append(imageROI_orig)
#     return img_orig,listOI,cnts



# imgg,L,tuplee = Crush("frame.jpg")
# Do_an.Getlist(Do_an,imgg,L,tuplee)
# app = QApplication(sys.argv)

# # create and show mainWindow
# doan = Do_an()
# doan.show()

# sys.exit(app.exec_())