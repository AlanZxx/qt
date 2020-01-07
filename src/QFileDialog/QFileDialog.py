from PyQt5.QtCore import *
from PyQt5.QtWidgets import  *
from PyQt5.QtGui import *
import  sys

class QfileDialogDemo(QWidget):
    def __init__(self):
        super(QfileDialogDemo, self).__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.button1 = QPushButton('选择图片')
        self.button1.clicked.connect(self.loadImage)
        layout.addWidget(self.button1)

        self.imageLable = QLabel()
        layout.addWidget(self.imageLable)

        self.button2  = QPushButton('加载文本文件')
        self.button2.clicked.connect(self.loadText)
        layout.addWidget(self.button2)

        self.contents = QTextEdit()
        layout.addWidget(self.contents)

        self.setLayout(layout)
        self.setWindowTitle("文件对话框演示")
        # self.resize(500, 500)

    def loadImage(self):
        fname, _=QFileDialog.getOpenFileName(self, "打开文件", '.', '图像文件(*.jpg *.png)')
        self.imageLable.setPixmap(QPixmap(fname))

    def loadText(self):
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.AnyFile)
        dialog.setFilter(QDir.Files)

        if dialog.exec():
            print("dakai1")
            filenames = dialog.selectedFiles()
            print("dakai2")
            # 必须要加，不然会出现bug
            f = open(filenames[0],encoding='utf-8', mode='r')
            print("dakai3")
            with f:
                print("dakai4")
                data = f.read()
                print("dakai5")
                self.contents.setText(data)
                print("dakai6")
        # print("load text")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = QfileDialogDemo()
    main.show()
    sys.exit(app.exec_())