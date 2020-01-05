from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget,QFileDialog,QApplication,QLabel,QMainWindow,QPushButton,QVBoxLayout,QHBoxLayout
import sys
class MainForm(QWidget):
    def __init__(self):
        super(MainForm, self).__init__()
        self.initUI()

    def initUI(self):
        # 添加垂直布局
        self.displayV_L = QVBoxLayout()

        self.displayV_R = QVBoxLayout()

        layout = QVBoxLayout()
        # 左上
        self.photo_L = QLabel()
        # self.displayV_L.addWidget(self.photo_L)

        # 左下
        self.text_L = QLabel()
        # self.displayV_L.addWidget(self.text_L)

        # 右上
        self.photo_R = QLabel()
        # self.displayV_R.addWidget(self.photo_R)
        layout.addWidget(self.photo_R)
        # 右下
        self.btn_select = QPushButton("&选择图片")
        layout.addWidget(self.btn_select)
        # self.displayV_R.addWidget(self.btn_select)
        self.btn_select.clicked.connect(self.selectImg)


        # //添加总体布局
        self.display_main = QHBoxLayout()
        # self.display_main.addWidget(self.displayV_L)
        # self.display_main.addWidget(self.displayV_R)

        self.setLayout(layout)
        self.setWindowTitle("目标检测")


    def selectImg(self):
        file,_ = QFileDialog.getOpenFileName(self, "打开图片",'.','图像类别(*.png *.jpg)')
        self.photo_L.setPixmap(QPixmap(file))
        self.photo_R.setPixmap(QPixmap(file))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainForm()
    main.show()
    sys.exit(app.exec_())
