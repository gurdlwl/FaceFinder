import sys

from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget, QAction, qApp, QLabel, QGridLayout, QPushButton, \
    QFileDialog, QMessageBox, QVBoxLayout, QHBoxLayout, QWidget, QGroupBox
from PyQt5 import QtGui, QtCore, QtWidgets
from qtpy import QtGui


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
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

        self.mainImg = QLabel(self)
        self.mainImg.setMaximumSize(700, 500) # label 최대 width, height를 조절
        self.mainImg.setScaledContents(1) # Image를 label 크기에 맞게 조절. 1 : true, 0 : false. false인 경우, 이미지가 label 크기만큼만 나오고 잘린다.

        self.faceImg = QLabel(self)
        self.faceImg.setMaximumSize(400, 400)
        self.faceImg.setScaledContents(1)

        self.detectedFaceImg = QLabel(self)
        self.detectedFaceImg.setMaximumSize(400, 400)
        self.detectedFaceImg.setScaledContents(1)

        self.fileOpenBtn = QPushButton('Open Image File', self)
        self.fileOpenBtn.clicked.connect(self.fileOpenClickMethod)

        # BoxLayout
        # self.createBoxLayout()

        self.createGridLayout()
        self.setCentralWidget(self.horizontalGroupBox)

        self.setWindowTitle('Face Finder')
        self.setWindowIcon(QIcon(''))  # Icon path
        self.setGeometry(self.left, self.top, self.width, self.height)  # move, resize를 합쳐놓은 것
        self.setFixedSize(self.width, self.height) # 창 크기 고정
        # self.move(10, 10)
        # self.resize(1280, 720)

        self.show()


    def fileOpenClickMethod(self):
        filename = QFileDialog.getOpenFileName(self, 'Open File', '/', 'Image Files (*.png *.jpg)') # 파일을 Image Files(*.png *.jpg)에 맞는 파일만 불러온다.
        print('fileName: ' + filename[0])

        if filename[0]: # 만약 파일을 골랐으면
            pixmap = QtGui.QPixmap(filename[0])
            self.mainImg.setPixmap(QPixmap(pixmap))
            self.mainImg.resize(pixmap.width(), pixmap.height())
            self.grid_layout.addWidget(self.mainImg, 1, 0)

        # QMessageBox.about(self, "notice", "click!")


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
        self.horizontalGroupBox = QGroupBox("grid")

        self.grid_layout = QGridLayout()
        self.grid_layout.addWidget(self.fileOpenBtn, 1, 0)
        self.grid_layout.addWidget(self.faceImg, 1, 1)
        self.grid_layout.addWidget(self.detectedFaceImg, 2, 1)

        self.horizontalGroupBox.setLayout(self.grid_layout)


def main():
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()