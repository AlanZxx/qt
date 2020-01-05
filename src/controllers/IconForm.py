import sys
from PyQt5.QtWidgets import QMainWindow,QApplication
from PyQt5.QtGui import QIcon

# 窗口的setwindowIcon方法用于设置窗口的图标，只在windows中可用
# Qapplication中的setwindow方法用于设置主窗口的图标和一个用程序图标，但调用了串钩的setwindowIcon方法


class IconForm(QMainWindow):
    def __init__(self,parent=None):
        super(IconForm,self).__init__(parent)
        self.initUi()
    def initUi(self):
        # 设置主窗口的标题
        self.setGeometry(300,300,500,400)
        self.setWindowTitle("设置窗口的图标")
        # 设置窗口的图标
        self.setWindowIcon(QIcon('./image/1.jpg'))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # app.setWindowIcon(QIcon('./image/1.jpg'))
    main = IconForm()
    main.show()
    sys.exit(app.exec())