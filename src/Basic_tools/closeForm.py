import  sys
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication,QMainWindow,QDesktopWidget,QPushButton,QHBoxLayout,QWidget

class MainWindow(QMainWindow):
    def __init__(self,parent = None):
        super(MainWindow, self).__init__(parent)
        self.resize(500, 400)
        self.statusBar().showMessage("目标检测主程序", 5000)
        self.setWindowTitle("关闭窗口")

        self.btn1 = QPushButton("关闭主窗口")
        self.btn1.clicked.connect(self.btn_close)

        layout = QHBoxLayout()
        layout.addWidget(self.btn1)

        main_form = QWidget()
        main_form.setLayout(layout)
        self.setCentralWidget(main_form)

    def btn_close(self):
        # sender是发送信号的对象
        sender = self.sender()
        print(sender.text()+"被按下")
        qApp = QApplication.instance()
        qApp.quit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("./../image/1.jpg"))
    form = MainWindow()
    form.show()
    sys.exit(app.exec_())