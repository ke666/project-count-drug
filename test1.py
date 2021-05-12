import Detect as De
import cv2
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from giao_dien import *
imgg,L,tuplee = De.Crush('pic1.jpg')
Do_an.Getlist(Do_an,imgg,L,tuplee)
app = QApplication(sys.argv)

# create and show mainWindow
doan = Do_an()
doan.show()

sys.exit(app.exec_())