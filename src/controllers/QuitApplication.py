import sys
from PyQt5.QtWidgets import QHBoxLayout,QApplication,QWidget,QMainWindow,QPushButton

class QuitApplication(QMainWindow):
    def __init__(self):
        super(QuitApplication, self).__init__()
        self.resize(400,500)
        self.setWindowTitle("退出应用程序")

        # 添加按钮
        self.button1 = QPushButton("推出应用程序")
        # 将信号与操关联
        self.button1.clicked.connect(self.onClick_Button)

        layout =QHBoxLayout()
        layout.addWidget(self.button1)

        mainFrame = QWidget()
        mainFrame.setLayout(layout)

        self.setCentralWidget(mainFrame)


        # 按钮的点击事件（自定义的曹）
    def onClick_Button(self):
        sender = self.sender()
        print(sender.text()+"按钮被按下")
        app = QApplication.instance()
        # 退出应用程序
        app.quit()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = QuitApplication()
    main.show()

    sys.exit(app.exec_())