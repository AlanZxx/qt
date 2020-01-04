# QDesktopWidget

import sys
from PyQt5.QtWidgets import QApplication,QWidget,QDesktopWidget,QMainWindow
from PyQt5.QtGui import QIcon

class CenterForm(QMainWindow):
    def __init__(self,parent=None):
        super(CenterForm, self).__init__(parent)

        # 设置主窗口的标题
        self.setWindowTitle("第一个主窗口应用")
        # 设置窗口的尺寸
        self.resize(400, 300)

    def center(self):
        # 获取屏幕坐标
        screen = QDesktopWidget().screenGeometry()
        # 获取窗口坐标系
        size = self.geometry()

        newLeft = (screen.width()-size.width())/4
        newTop = (screen.height()-size.height())/4
        self.move(newLeft,newTop)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("./image/1.jpg"))
    main = CenterForm()
    main.show()
    sys.exit(app.exec())