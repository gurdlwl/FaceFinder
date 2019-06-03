import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget, QAction, qApp

class MyApp(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        exitAction = QAction('Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)

        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        fileMenu = menubar.addMenu('File')
        fileMenu.addAction(exitAction)

        self.setWindowTitle('Face Finder')
        self.setWindowIcon(QIcon('')) # Icon path
        self.setGeometry(100, 100, 1280, 720) # move, resize를 합쳐놓은 것
        # self.move(10, 10)
        # self.resize(1280, 720)
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())