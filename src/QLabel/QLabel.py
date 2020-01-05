import  sys
from PyQt5.QtWidgets import QVBoxLayout,QMainWindow,QApplication,QPushButton,QWidget,QLabel
from PyQt5.QtGui import QPalette,QPixmap
from PyQt5.QtCore import  Qt

class QlabelDemo(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    
    def initUI(self):
        label1 = QLabel(self)
        label2 = QLabel(self)
        label3 = QLabel(self)
        label4 = QLabel(self)

        label1.setText("<font color=yellow>这是一个文本标签.</font>")
        # 如果设置位true，则使用浏览器打开
        label1.setAutoFillBackground(True)
        palette = QPalette()
        palette.setColor(QPalette.Window,Qt.blue)
        label1.setPalette(palette)
        label1.setAlignment(Qt.AlignCenter)

        label2.setText("<a href='#'> 欢迎使用Python GUI编程</a>")

        label3.setAlignment(Qt.AlignCenter)
        label3.setToolTip("这是标签")
        label3.setPixmap(QPixmap('./../image/1.jpg'))

        label4.setOpenExternalLinks(True)
        label4.setText("<a href='http://item.jd.com/12417265.html'>感谢关注《xxx》</a>")
        label4.setAlignment(Qt.AlignRight)
        label4.setToolTip("这是一个超链接")

        vbox = QVBoxLayout()
        vbox.addWidget(label1)
        vbox.addWidget(label2)
        vbox.addWidget(label3)
        vbox.addWidget(label4)

        label2.linkHovered.connect(self.linkHovered)
        label4.linkActivated.connect(self.linkClicked)

        self.setLayout(vbox)
        self.setWindowTitle("Qlabel控件演示")

    def linkHovered(self):
        print("当鼠标滑过label2")

    def linkClicked(self):
        print("labtl4单机，触发")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = QlabelDemo()
    main.show()
    sys.exit(app.exec_())


