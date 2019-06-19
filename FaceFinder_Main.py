import sys

from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget, QAction, qApp, QLabel, QGridLayout, QPushButton, \
    QFileDialog, QMessageBox, QVBoxLayout, QHBoxLayout, QWidget, QGroupBox
from PyQt5 import QtGui, QtCore, QtWidgets
from qtpy import QtGui
import functools

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

        '''
        exitAction = QAction('Exit', self)
        exitAction.setShortcut('Esc')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.)

        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        fileMenu = menubar.addMenu('File')
        fileMenu.addAction(exitAction)
        '''

        self.mainImg = QLabel(self) # main사진이 들어갈 Label
        self.mainImg.setObjectName('mainImg')
        self.mainImg.setMaximumSize(700, 500) # label 최대 width, height를 조절
        self.mainImg.setScaledContents(1) # Image를 label 크기에 맞게 조절. 1 : true, 0 : false. false인 경우, 이미지가 label 크기만큼만 나오고 잘린다.

        self.faceImg = QLabel(self) # 얼굴사진이 들어갈 Label
        self.faceImg.setObjectName('faceImg')
        self.faceImg.setMaximumSize(400, 400)
        self.faceImg.setScaledContents(1)

        self.detectedFaceImg = QLabel(self) # main에서 찾은 얼굴사진이 들어갈 Label
        self.detectedFaceImg.setMaximumSize(400, 400)
        self.detectedFaceImg.setScaledContents(1)

        # image Click Event 설정
        self.mainImg.mousePressEvent = functools.partial(MainWindow.fileOpenMethod, self.mainImg)
        self.faceImg.mousePressEvent = functools.partial(MainWindow.fileOpenMethod, self.faceImg)

        # self.fileOpenBtn = QPushButton('Open Image File', self)
        # self.fileOpenBtn.setMaximumWidth(150)
        # self.fileOpenBtn.clicked.connect(self.fileOpenClickMethod)

        # 일단 임시로 image 넣어놓음
        baseImg = QtGui.QPixmap('D:/사진/캡처.PNG')
        self.mainImg.setPixmap(baseImg)
        self.faceImg.setPixmap(baseImg)
        self.detectedFaceImg.setPixmap(baseImg)

        self.createGridLayout()
        self.setCentralWidget(self.horizontalGroupBox)

        self.setWindowTitle('Face Finder')
        self.setWindowIcon(QIcon(''))  # Icon path
        # self.move(10, 10)
        # self.resize(1280, 720)
        self.setGeometry(self.left, self.top, self.width, self.height)  # move, resize를 합쳐놓은 것
        self.setFixedSize(self.width, self.height) # 창 크기 고정

        self.show()


    def fileOpenMethod(self, event):
        filename = QFileDialog.getOpenFileName(self, 'Open File', '/', 'Image Files (*.png *.jpg)')

        print('called by: ' + str(self.objectName()))
        print('fileName: ' + filename[0])

        if filename[0]: # 만약 파일을 골랐으면
            pixmap = QtGui.QPixmap(filename[0])
            self.setPixmap(QPixmap(pixmap))
            self.resize(pixmap.width(), pixmap.height())

        if(str(self.objectName()) == 'mainImg') :
            print('hahaha I find it')
            # 해당 파일 넘겨줘서 face recognition


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
        # grid_layout.addWidget( WIDGET, 행, 열 )
        self.grid_layout.addWidget(self.mainImg, 0, 0)
        # self.grid_layout.addWidget(self.fileOpenBtn, 0, 0)
        self.grid_layout.addWidget(self.faceImg, 0, 1)
        self.grid_layout.addWidget(self.detectedFaceImg, 1, 1)

        self.horizontalGroupBox.setLayout(self.grid_layout)


def main():
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()