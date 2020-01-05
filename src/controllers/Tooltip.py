import sys

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QMainWindow,QApplication,QHBoxLayout,QToolTip,QPushButton,QWidget

class Tooltip(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        QToolTip.setFont(QFont('ScansSerif', 12))
        self.setToolTip("今天是<b>星期五</b>")
        self.setGeometry(300,300,300,600)
        self.setWindowTitle("设置控件提示信息")

        self.buttin1 = QPushButton('我的按钮')
        self.buttin1.setToolTip("这是一个按钮，ARE you ok？")

        layout = QHBoxLayout()
        layout.addWidget(self.buttin1)
        mainFrame = QWidget()
        mainFrame.setLayout(layout)

        self.setCentralWidget(mainFrame)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # app.setWindowIcon(QIcon('./image/1.jpg'))
    main = Tooltip()
    main.show()
    sys.exit(app.exec())