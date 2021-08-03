####file main
import Detect as De
import cv2
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from giao_dien import *

#get video/imagin from camera
vidcap = cv2.VideoCapture('video.mp4')
#vidcap = cv2.VideoCapture(0)
#vidcap = cv2.VideoCapture('http://192.168.1.103:8080/video')
success, image =  vidcap.read()
count = 0
success = True
while success:

    # cv2.imwrite("frame%d.jpg" % count, image)
    cv2.imwrite("frame20.jpg" ,image)
    success, image = vidcap.read()
    print('read a new frame:', success)
    count += 1
    if count > 10:
        break


imgg,L,tuplee = De.Crush('frame20.jpg')
Do_an.Getlist(Do_an,imgg,L,tuplee)
app = QApplication(sys.argv)

# create and show mainWindow
doan = Do_an()
doan.show()

sys.exit(app.exec_())