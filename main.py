from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog, QLabel
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QPixmap, QPainter, QPen
from pdf2image import convert_from_path
from PIL import Image
import os
import sys

class MyLabel(QLabel):
    x0 = 0
    y0 = 0
    x1 = 0
    y1 = 0
    flag = False

    def mousePressEvent(self,event):
        self.flag = True
        self.x0 = event.x()
        self.y0 = event.y()

    def mouseReleaseEvent(self,event):
        self.flag = False

    def mouseMoveEvent(self,event):
        if self.flag:
            self.x1 = event.x()
            self.y1 = event.y()
            self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        rect = QRect(self.x0, self.y0, self.x1-self.x0, self.y1-self.y0)
        painter = QPainter(self)
        painter.setPen(QPen(Qt.red, 2, Qt.SolidLine))
        painter.drawRect(rect)

class Ui_MainWindow(QMainWindow):
    def __init__(self):
        super(Ui_MainWindow, self).__init__()

        self.setObjectName("MainWindow")
        self.resize(827, 1270)
        self.setStyleSheet("background-color: rgb(255, 235, 160);color: rgb(10, 10, 10);")
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")

        self.label = MyLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 50, 827, 1170))
        self.label.setStyleSheet("background-color: rgb(242, 255, 223);color: rgb(10, 10, 10);")
        self.label.setObjectName("label")

        self.btn_open = QtWidgets.QPushButton(self.centralwidget)
        self.btn_open.setGeometry(QtCore.QRect(20, 10, 131, 31))
        self.btn_open.setStyleSheet("background-color: rgb(254, 208, 178);")
        self.btn_open.setObjectName("btn_open")

        self.btn_right = QtWidgets.QPushButton(self.centralwidget)
        self.btn_right.setGeometry(QtCore.QRect(670, 10, 113, 32))
        self.btn_right.setStyleSheet("background-color: rgb(254, 208, 178);")
        self.btn_right.setObjectName("btn_right")

        self.btn_left = QtWidgets.QPushButton(self.centralwidget)
        self.btn_left.setGeometry(QtCore.QRect(520, 10, 113, 32))
        self.btn_left.setStyleSheet("background-color: rgb(254, 208, 178);")
        self.btn_left.setObjectName("btn_left")
        self.setCentralWidget(self.centralwidget)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)
        self.clearJPGfiles()
        self.add_functions()
        self.n = 0
        self.pages = 0
        self.size

    def clearJPGfiles(self):
        for file in os.listdir(os.getcwd ()):
            if file.endswith('.jpg'):
                os.remove(file)

    def closeEvent(self, event):
        close = QMessageBox()
        close.setText("You sure?")
        close.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
        close = close.exec()

        if close == QMessageBox.Yes:
            self.clearJPGfiles()
            event.accept()
        else:
            event.ignore()


    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "Тест_Ваганов_А_М"))
        self.label.setText(_translate("MainWindow", "Тут будет файл"))
        self.btn_open.setText(_translate("MainWindow", "Open File"))
        self.btn_right.setText(_translate("MainWindow", ">"))
        self.btn_left.setText(_translate("MainWindow", "<"))

    def add_functions(self):
        self.btn_open.clicked.connect(self.open_file)
        self.btn_right.clicked.connect(self.right)
        self.btn_left.clicked.connect(self.left)

    def open_file(self):
        self.clearJPGfiles()
        c = 0
        fname = QFileDialog.getOpenFileName(self, 'Open File', '/', 'PDF File (*.pdf)')[0]
        path = "{}" "".format(fname)
        try:
            images = convert_from_path(path)
            self.pages = len(images)
            for i in images:
                i.save(str(c) + ".jpg")
                c = c + 1

            with Image.open("0.jpg") as img:
                self.width = img.width
                self.height = img.height
            pixmap = QPixmap("0.jpg")
            smaller_pixmap = pixmap.scaled(int(self.width/2), int(self.height/2))
            self.label.setPixmap(smaller_pixmap)
            self.label.resize(pixmap.width(), pixmap.height())
            self.label.setAlignment(QtCore.Qt.AlignLeft)
            self.resize(int(self.width/2) + 50, int(self.height/2) + 100)

        except FileNotFoundError:
            print("No such file")

    def right(self):
        if self.n+1 != self.pages:
            try:
                with Image.open(str(self.n + 1) + ".jpg") as img:
                    self.width = img.width
                    self.height = img.height
                pixmap = QPixmap(str(self.n + 1) + ".jpg")
                smaller_pixmap = pixmap.scaled(int(self.width/2), int(self.height/2))
                self.label.setPixmap(smaller_pixmap)
                self.label.setAlignment(QtCore.Qt.AlignLeft)
                self.n = self.n + 1
            except:
                print("Конец")
        else:
            print(self.pages, self.n)

    def left(self):
        if self.n > 0:
            try:
                with Image.open(str(self.n - 1) + ".jpg") as img:
                    self.width = img.width
                    self.height = img.height
                pixmap = QPixmap(str(self.n - 1) + ".jpg")
                smaller_pixmap = pixmap.scaled(int(self.width/2), int(self.height/2))
                self.label.setPixmap(smaller_pixmap)
                self.label.setAlignment(QtCore.Qt.AlignLeft)
                self.n = self.n - 1
            except:
                print("Конец")
        else:
            print(self.pages, self.n)

def application():
    app = QApplication(sys.argv)
    window = Ui_MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    application()