import sys

from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget, QAction, qApp, QLabel, QGridLayout, QPushButton, \
    QFileDialog, QMessageBox, QVBoxLayout, QHBoxLayout, QWidget, QGroupBox
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import Qt
from qtpy import QtGui
import functools
import dlib, cv2

face_detector = dlib.get_frontal_face_detector()
shape_predicter = dlib.shape_predictor('Models/shape_predictor_68_face_landmarks.dat')
face_recognition_model = dlib.face_recognition_model_v1('Models/dlib_face_recognition_resnet_model_v1.dat')

#허용 오차 범위
TOLERANCE = 0.5



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
        self.setObjectName('default')

        self.defaultLabelSetting() # QLabel default 설정
        self.setBaseImg() # QLabel base Image 설정
        self.setBaseMenuBar() # MenuBar 설정

        self.createGridLayout()
        self.setCentralWidget(self.horizontalGroupBox)

        self.setWindowTitle('Face Finder')
        self.setWindowIcon(QIcon(''))  # Icon path
        self.setStyleSheet('background-color: rgb(255, 255, 255)')
        self.setGeometry(self.left, self.top, self.width, self.height)  # move, resize를 합쳐놓은 것
        self.setFixedSize(self.width, self.height) # 창 크기 고정

        self.show()


    def defaultLabelSetting(self):
        self.mainImg = QLabel(self)  # main사진이 들어갈 Label
        self.mainImg.setObjectName('mainImg')
        self.mainImg.setMaximumSize(910, 910)  # label 최대 width, height를 조절
        self.mainImg.setAlignment(Qt.AlignCenter)
        # self.mainImg.setScaledContents(1)

        self.faceImg = QLabel(self)  # 얼굴사진이 들어갈 Label
        self.faceImg.setObjectName('faceImg')
        self.faceImg.setMinimumSize(420, 420)
        self.faceImg.setMaximumSize(420, 420)
        self.faceImg.setAlignment(Qt.AlignCenter)
        self.faceImg.setScaledContents(1)  # Image를 label 크기에 맞게 조절. 1 : true, 0 : false. false인 경우, 만약 이미지가 label크기보다 크다면 이미지가 label 크기만큼만 나오고 잘린다.

        self.detectedFaceImg = QLabel(self)  # main에서 찾은 얼굴사진이 들어갈 Label
        self.detectedFaceImg.setMinimumSize(420, 420)
        self.detectedFaceImg.setMaximumSize(420, 420)
        self.detectedFaceImg.setScaledContents(1)

        # image Click Event 설정
        # self.WIDGET.mousePressEvent = functools.partial(Method, WIDGET)
        self.mainImg.mousePressEvent = functools.partial(MainWindow.fileOpenMethod, self.mainImg)
        self.faceImg.mousePressEvent = functools.partial(MainWindow.fileOpenMethod, self.faceImg)


    def setBaseMenuBar(self):
        exitAction = QAction('Exit', self)
        exitAction.setShortcut('Esc')
        exitAction.setStatusTip('Exit Application')
        exitAction.triggered.connect(qApp.quit)

        refreshAction = QAction('Refresh', self)
        refreshAction.setShortcut('Ctrl+F5')
        refreshAction.setStatusTip('Refresh Screen')
        refreshAction.triggered.connect(self.setBaseImg)

        detectAction = QAction('Face Detect Mode', self)
        detectAction.setShortcut('Ctrl+1')
        detectAction.setStatusTip('Change Mode to Face Detect')
        detectAction.triggered.connect(self.face_detection_Mode)

        recognizeAction = QAction('Face Recognize Mode (To be developed)', self)
        recognizeAction.setShortcut('Ctrl+2')
        recognizeAction.setStatusTip('Change Mode to Face Detect')
        recognizeAction.triggered.connect(self.face_recognition_Mode)

        menubar = self.menuBar()
        Menu = menubar.addMenu('Menu')
        Menu.addAction(exitAction)
        Menu.addAction(refreshAction)
        Mode = menubar.addMenu('Mode')
        Mode.addAction(detectAction)
        Mode.addAction(recognizeAction)


    def setBaseImg(self):
        # 일단 임시로 image 넣어놓음
        baseImg = QtGui.QPixmap('Images/capture.png')

        self.mainImg.setPixmap(baseImg)
        self.mainImg.setText('Click Here!')
        self.mainImg.setStyleSheet('border: 1px solid black')

        self.faceImg.setPixmap(baseImg)
        self.faceImg.setText('Click Here!')
        self.faceImg.setStyleSheet('border: 1px solid black')

        self.detectedFaceImg.setPixmap(baseImg)
        self.detectedFaceImg.setStyleSheet('border: 1px solid black')


    def fileOpenMethod(self, event):
        # path에 한글포함 하지말것
        filename = QFileDialog.getOpenFileName(self, 'Open File', '/', 'Image Files (*.png *.jpg)')

        if filename[0]: # 파일을 골랐으면
            mode = str(self.parent().parent().objectName())
            labelName = str(self.objectName())

            pixmap = QtGui.QPixmap(filename[0])
            self.setPixmap(QPixmap(pixmap))
            self.resize(pixmap.width(), pixmap.height())

            print('called by: ' + str(self.objectName()))
            print('fileName: ' + filename[0])
            print('Mode : ' + mode)

            # mode와 labelName 확인 후 해당 파일 넘겨줘서 detection, face recognition
            if mode == 'default' or mode == 'detection' :
                if labelName == 'mainImg' :
                    MainWindow.face_detection(self, filename[0])

            if mode == 'recognition' :
                if labelName == 'faceImg' :
                    MainWindow.face_recognition(self, filename[0])
                if labelName == 'mainImg' :
                    MainWindow.face_recognition(self, filename[0])

        if not filename[0]: # 파일을 고르지 않았다면
            print('Please Select Image')


    def createGridLayout(self):
        self.horizontalGroupBox = QGroupBox('Face Finder')

        self.grid_layout = QGridLayout()
        self.grid_layout.addWidget(self.faceImg, 0, 0)
        self.grid_layout.addWidget(self.detectedFaceImg, 1, 0)

        self.grid_layout2 = QGridLayout()
        self.grid_layout2.addWidget(self.mainImg, 0, 0)
        self.grid_layout2.addLayout(self.grid_layout, 0, 1)

        self.horizontalGroupBox.setLayout(self.grid_layout2)


    def face_detection_Mode(self):
        self.setObjectName('detection')
        print('mode change : ' + self.objectName())


    def face_recognition_Mode(self):
        self.setObjectName('recognition')
        print('mode change : ' + self.objectName())


    def face_detection(self, path):
        print('\n* * * Face Detection Start * * *')

        img = cv2.cvtColor(dlib.load_rgb_image(path), cv2.COLOR_BGR2RGB) # Image 불러올 때 BGR로 불러옴. 바꿔주기 위해서 cv2.COLOR_BGR2RGB 사용
        dets = face_detector(img, 3) # (img, INT) 숫자가 높을수록 face detect 정확도 올라감 but 속도 저하

        if len(dets) == 0 :
            print('No faces found.')

        if len(dets) > 0 :
            print('Number of faces detected: {}'.format(len(dets)))
            for i, d in enumerate(dets): # i = index, d = 찾은 얼굴 좌표
                print('People {}: Left {}, Top {}, Right {}, Bottom {}'.format(i+1, d.left(), d.top(), d.right(), d.bottom()))

                crop = img[d.top():d.bottom(),d.left():d.right()]
                outPath = "Result/{}_detected.jpg".format(i+1)
                cv2.imwrite(outPath, crop)

                cv2.rectangle(img, (d.left(), d.top()), (d.right(), d.bottom()), (0, 0, 255), 2)

            cv2.imwrite("Result/all.jpg", img)

            detectedImg = QtGui.QPixmap('Result/all.jpg')
            self.parent().parent().detectedFaceImg.setPixmap(detectedImg)

        print('* * * Face Detection Finish * * *\n')


    def face_recognition(self, path):
        print('\n* * * Face Recognition Start * * *')

        img = cv2.cvtColor(dlib.load_rgb_image(path), cv2.COLOR_BGR2RGB)
        dets = face_detector(img, 3)

        if len(dets) == 0 :
            print('No Face Found.')

        if len(dets) > 0 :
            print('hi')


        print('* * * Face Recognition Finish * * *\n')


def main():
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()