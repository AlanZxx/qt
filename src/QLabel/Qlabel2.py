from PyQt5.QtWidgets import *
import  sys

# mainLayout.addWidget(nameLabel, 0, 0，0，0)
# 控件对象，所要放置的行列，以及占用的行列个数
class Qlabel2(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        self.setWindowTitle("Qlabel与伙伴控制")

        nameLabel = QLabel('&Name',self)
        nameLineEdit = QLineEdit(self)
        # 设置了伙伴控件
        nameLabel.setBuddy(nameLineEdit)


        passwordLabel = QLabel('&Passwprd',self)
        passwordEdit = QLineEdit(self)
        # 设置了伙伴控件
        passwordLabel.setBuddy(passwordEdit)

        btn = QPushButton('&OK')
        btnCancel = QPushButton("&Cancel")

        mainLayout = QGridLayout(self)
        mainLayout.addWidget(nameLabel,0,0)
        mainLayout.addWidget(nameLineEdit,0,1,1,2)
        # 行列，占用几行几列

        mainLayout.addWidget(passwordLabel,1,0)
        mainLayout.addWidget(passwordEdit,1,1,1,2)

        mainLayout.addWidget(btn,2,1)
        mainLayout.addWidget(btnCancel,2,2)

if __name__ == '__main__':
    app =QApplication(sys.argv)
    main = Qlabel2()
    main.show()
    sys.exit(app.exec_())