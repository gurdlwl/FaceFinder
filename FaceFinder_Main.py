import sys

from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget, QAction, qApp, QLabel, QGridLayout, QPushButton, \
    QFileDialog, QMessageBox, QVBoxLayout, QHBoxLayout, QWidget, QGroupBox
from PyQt5 import QtGui, QtCore, QtWidgets
from qtpy import QtGui
import functools
import dlib, cv2

face_detector = dlib.get_frontal_face_detector()

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        # left, top, width, height 변수 정의&초기화
        self.left = 100
        self.top = 100
        self.width = 1600
        self.height = 900

        self.initUI()


    def initUI(self):
        self.setBaseMenuBar() # MenuBar 설정

        self.mainImg = QLabel(self) # main사진이 들어갈 Label
        self.mainImg.setObjectName('mainImg')
        self.mainImg.setMaximumSize(910, 910) # label 최대 width, height를 조절
        self.mainImg.setScaledContents(1) # Image를 label 크기에 맞게 조절. 1 : true, 0 : false. false인 경우, 만약 이미지가 label크기보다 크다면 이미지가 label 크기만큼만 나오고 잘린다.

        self.faceImg = QLabel(self) # 얼굴사진이 들어갈 Label
        self.faceImg.setObjectName('faceImg')
        self.faceImg.setMinimumSize(420, 420)
        self.faceImg.setMaximumSize(420, 420)
        self.faceImg.setScaledContents(1)

        self.detectedFaceImg = QLabel(self) # main에서 찾은 얼굴사진이 들어갈 Label
        self.detectedFaceImg.setMinimumSize(420, 420)
        self.detectedFaceImg.setMaximumSize(420, 420)
        self.detectedFaceImg.setScaledContents(1)

        # image Click Event 설정
        # self.WIDGET.mousePressEvent = functools.partial(Method, WIDGET)
        self.mainImg.mousePressEvent = functools.partial(MainWindow.fileOpenMethod, self.mainImg)
        self.faceImg.mousePressEvent = functools.partial(MainWindow.fileOpenMethod, self.faceImg)

        self.setBaseImg()

        self.createGridLayout()
        self.setCentralWidget(self.horizontalGroupBox)

        self.setWindowTitle('Face Finder')
        self.setWindowIcon(QIcon(''))  # Icon path
        self.setGeometry(self.left, self.top, self.width, self.height)  # move, resize를 합쳐놓은 것
        self.setFixedSize(self.width, self.height) # 창 크기 고정

        self.show()


    def setBaseMenuBar(self):
        exitAction = QAction('Exit', self)
        exitAction.setShortcut('Esc')
        exitAction.setStatusTip('Exit Application')
        exitAction.triggered.connect(qApp.quit)

        refreshAction = QAction('Refresh', self)
        refreshAction.setShortcut('Ctrl+F5')
        refreshAction.setStatusTip('Refresh Screen')
        refreshAction.triggered.connect(self.setBaseImg)

        detectAction = QAction('Face Detect Mode (To be developed)', self)
        detectAction.setShortcut('Ctrl+1')
        detectAction.setStatusTip('Change Mode to Face Detect')
        # detectAction.triggered.connect()

        recognizeAction = QAction('Face Recognize Mode (To be developed)', self)
        recognizeAction.setShortcut('Ctrl+2')
        recognizeAction.setStatusTip('Change Mode to Face Detect')
        # recognizeAction.triggered.connect()

        menubar = self.menuBar()
        Menu = menubar.addMenu('Menu')
        Menu.addAction(exitAction)
        Menu.addAction(refreshAction)
        Mode = menubar.addMenu('Mode')
        Mode.addAction(detectAction)
        Mode.addAction(recognizeAction)


    def setBaseImg(self):
        # 일단 임시로 image 넣어놓음
        baseImg = QtGui.QPixmap('D:/사진/캡처.PNG')
        self.mainImg.setPixmap(baseImg)
        self.faceImg.setPixmap(baseImg)
        self.detectedFaceImg.setPixmap(baseImg)


    def fileOpenMethod(self, event):
        # path에 한글포함 하지말것
        filename = QFileDialog.getOpenFileName(self, 'Open File', '/', 'Image Files (*.png *.jpg)')

        if filename[0]: # 만약 파일을 골랐으면
            print('called by: ' + str(self.objectName()))
            print('fileName: ' + filename[0])

            pixmap = QtGui.QPixmap(filename[0])
            self.setPixmap(QPixmap(pixmap))
            self.resize(pixmap.width(), pixmap.height())

            if(str(self.objectName()) == 'mainImg') :
                MainWindow.face_detection(filename[0])
                # 해당 파일 넘겨줘서 face recognition, detection

        if not filename[0]:
            print('Please Select Image')


    def createBoxLayout(self):
        horizontal_layout = QtWidgets.QHBoxLayout()
        horizontal_layout.addWidget(self.label)
        horizontal_layout.addWidget(self.fileOpenBtn)

        vertical_layout = QtWidgets.QVBoxLayout()
        vertical_layout.addLayout(horizontal_layout)

        box_layout = QtWidgets.QWidget()
        box_layout.setLayout(vertical_layout)

        self.setCentralWidget(box_layout)


    def createGridLayout(self):
        self.horizontalGroupBox = QGroupBox("face finder")

        self.grid_layout = QGridLayout()
        self.grid_layout.addWidget(self.faceImg, 0, 0)
        self.grid_layout.addWidget(self.detectedFaceImg, 1, 0)

        self.grid_layout2 = QGridLayout()
        self.grid_layout2.addWidget(self.mainImg, 0, 0)
        self.grid_layout2.addLayout(self.grid_layout, 0, 1)

        self.horizontalGroupBox.setLayout(self.grid_layout2)


    def face_detection(path):
        print('* * * Face Detection Start * * *')

        img = cv2.cvtColor(dlib.load_rgb_image(path), cv2.COLOR_BGR2RGB) # Image 불러올 때 BGR로 불러옴. 바꿔주기 위해서 cv2.COLOR_BGR2RGB 사용
        dets = face_detector(img, 1) # (img, INT) 숫자가 높을수록 face detect 정확도 올라감 but 속도 저하

        print('Number of faces detected: {}'.format(len(dets)))
        for i, d in enumerate(dets):
            print('People {}: Left {}, Top {}, Right {}, Bottom {}'.format(i+1, d.left(), d.top(), d.right(), d.bottom()))

            crop = img[d.top():d.bottom(),d.left():d.right()]
            outPath = "Result/{}_detected.jpg".format(i+1)
            cv2.imwrite(outPath, crop)

            cv2.rectangle(img, (d.left(), d.top()), (d.right(), d.bottom()), (0, 0, 255), 1)

        win = dlib.image_window()
        win.set_image(img)
        win.add_overlay(dets)
        cv2.imwrite("Result/all.jpg", img)

        print('* * * Face Detection Finish * * *')

    # def face_recognition():


def main():
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()