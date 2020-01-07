from PyQt5.QtWidgets import QApplication,QWidget,QGridLayout,QLabel,QPushButton,QRadioButton,QFileDialog,QDialog
from PyQt5.QtGui import QIcon,QPixmap
from PyQt5.QtCore import Qt
import sys

# 0表示文件,1表示文件夹
global file_or_folder_status
global path
path = None
file_or_folder_status = 0
class MainWindow(QWidget):
    def __init__(self,parent = None):
        super(MainWindow, self).__init__(parent)
        self.initUI()
        self.initListener()

    def initUI(self):
        # self.setGeometry(300,300,250,150)
        self.resize(600,400)

        self.label_left = QLabel()
        self.label_left.setText("检测文件夹结果详情")
        # self.label_left.setPixmap(QPixmap("./../image/1.jpg"))
        self.label_middle1 = QLabel()
        self.label_middle1.setText("原图片/图片集")
        # self.label_middle1.setPixmap(QPixmap("./../image/1.jpg"))


        self.label_middle2 = QLabel()
        # self.label_middle2.setPixmap(QPixmap("./../image/1.jpg"))
        self.label_middle2.setText("结果图片/图片集")

        self.label_right1 = QLabel()
        self.label_right1.setText("目标详情")

        self.label_right2 = QLabel()
        self.label_right2.setText("文件/文件夹路径")

        self.radio1 = QRadioButton("文件")
        self.radio1.setChecked(True)

        self.radio2 = QRadioButton("文件夹")

        # self.btn1_select_photo = QPushButton("选择文件")
        # self.btn2_select_folder = QPushButton("选择文件夹")
        self.select  = QPushButton("选择文件/文件夹")
        self.btn_send = QPushButton("开始检测")
        mainLayout = QGridLayout()
        mainLayout.addWidget(self.label_left,0,0,10,3)
        mainLayout.addWidget(self.label_middle1,0,3,5,5)
        mainLayout.addWidget(self.label_middle2,5,3,5,5)

        mainLayout.addWidget(self.label_right1,0,8,6,2)
        mainLayout.addWidget(self.label_right2,6,8,1,2)
        mainLayout.addWidget(self.radio1,7,8,1,1)
        mainLayout.addWidget(self.radio2,7,9,1,1)
        mainLayout.addWidget(self.select,8,8,1,2)
        # mainLayout.addWidget(self.btn1_select_photo,8,8,1,1)
        # mainLayout.addWidget(self.btn2_select_folder,8,9,1,1)
        mainLayout.addWidget(self.btn_send,9,8,1,2)

        self.setWindowTitle("目标检测主窗口")
        self.setWindowIcon(QIcon("./../image/excavator.ico"))
        self.setLayout(mainLayout)

    # 监听事件
    def initListener(self):
        # 两个radiobutton的事件
        self.radio1.toggled.connect(lambda :self.btnstate(self.radio1))
        self.radio2.toggled.connect(lambda :self.btnstate(self.radio2))

    #     添加选择文件/文件夹的标签
        self.select.clicked.connect(self.loadImage)
    #     开始检测按钮
        self.btn_send.clicked.connect(self.startDetect)
    def startDetect(self):
        global file_or_folder_status
        global path
        # path = 2
        # //检测某一个文件
        if path is None:
            self.showDialog("path is invalid")
        if file_or_folder_status==0:
            print("开始检测文件："+path)
        elif file_or_folder_status==1:
            print("开始检测文件夹："+path)
        else:
            print("文件/文件夹状态异常")
    #     加载图片槽
    def loadImage(self):
        global path
        fname, _ = QFileDialog.getOpenFileName(self, "打开文件", '.', '图像文件(*.jpg *.png)')
        path = fname
        # print(path)
        self.label_right2.setText(path)
        self.label_middle1.setPixmap(QPixmap(fname))
    # QRadioButton事件
    def btnstate(self,btn):
        global file_or_folder_status
        if btn.text()=="文件":
            if btn.isChecked()==True:
                # print(btn.text()+"is selected")
                file_or_folder_status = 0;
                print(file_or_folder_status)
            # else:
                # print(btn.text()+"is not selected")

        if btn.text()=="文件夹":
            if btn.isChecked()==True:
                file_or_folder_status = 1;
                print(file_or_folder_status)
                # print(btn.text()+"is selected")
            # else:
                # print(btn.text()+"is not selected")
    def showDialog(self,paramater):
        dialog = QDialog()
        text = QLabel(paramater, dialog)
        btn  = QPushButton("ok", dialog)
        dialog.setWindowTitle("错误提示")
        dialog.setWindowModality(Qt.ApplicationModal   )
        dialog.exec_()
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())