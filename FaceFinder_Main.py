import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget, QAction, qApp, QLabel, QGridLayout, QPushButton, \
    QFileDialog, QMessageBox
from qtpy import QtGui


class MyApp(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        exitAction = QAction('Exit', self)
        exitAction.setShortcut('Esc')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)

        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        fileMenu = menubar.addMenu('File')
        fileMenu.addAction(exitAction)

        self.setWindowTitle('Face Finder')
        self.setWindowIcon(QIcon('')) # Icon path
        self.setGeometry(100, 100, 1600, 900) # move, resize를 합쳐놓은 것
        # self.setFixedSize(1680, 900) # 창 크기 고정
        # self.move(10, 10)
        # self.resize(1280, 720)

        self.label = QLabel(self)
        self.label.move(200, 200)

        fileOpenBtn = QPushButton('Open Image File', self)
        fileOpenBtn.move(800, 450)
        fileOpenBtn.clicked.connect(self.fileOpenBtnClickMethod)

        self.show()

    def fileOpenBtnClickMethod(self):
        filename = QFileDialog.getOpenFileName(self, 'Open File', '/', 'Image Files(*.png *.jpg)')
        print(filename)

        if filename[0]:
            pixmap = QtGui.QPixmap(filename[0])
            self.label.setPixmap(QPixmap(pixmap))
            self.label.resize(pixmap.width(), pixmap.height())
        # QMessageBox.about(self, "notice", "click!")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())