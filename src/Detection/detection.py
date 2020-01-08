from PyQt5.QtWidgets import QApplication,QTextEdit,QDesktopWidget,QMessageBox,QWidget,QGridLayout,QLabel,QPushButton,QRadioButton,QFileDialog,QDialog
from PyQt5.QtGui import QIcon,QPixmap
from PyQt5.QtCore import Qt,QDir,QSize
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
        desktop = QApplication.desktop()
        # self.setGeometry(300,300,250,150)
        self.resize(desktop.width()*3/4, desktop.height()*3/4)

        self.label_left = QLabel()
        self.label_left.setText("检测文件夹结果详情")
        self.label_middle1 = QLabel()
        self.label_middle1.setText("原图片/图片集")


        self.label_middle2 = QLabel()
        # self.label_middle2.setPixmap(QPixmap("./../image/1.jpg"))
        self.label_middle2.setText("结果图片/图片集")

        self.label_right1 = QTextEdit()
        self.label_right1.setText("目标详情")

        self.label_right2 = QLabel()
        self.label_right2.setText("文件/文件夹路径")

        self.status = QTextEdit()
        self.status.setText("就绪")
        # self.status.setEnabled(False)

        self.radio1 = QRadioButton("文件")
        self.radio1.setChecked(True)

        self.radio2 = QRadioButton("文件夹")

        # self.btn1_select_photo = QPushButton("选择文件")
        # self.btn2_select_folder = QPushButton("选择文件夹")
        self.select  = QPushButton("选择文件/文件夹")
        self.btn_send = QPushButton("开始检测")
        mainLayout = QGridLayout()
        mainLayout.addWidget(self.label_left,0,0,8,3)
        mainLayout.addWidget(self.status,8,0,2,3)
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
        self.status.setText("请选择文件.....")
        self.select.clicked.connect(self.loadImage)
    #     开始检测按钮
        self.btn_send.clicked.connect(self.startDetect)
    def startDetect(self):
        global file_or_folder_status
        global path
        # path = 2
        # //检测某一个文件
        if path is None:
            self.showDialog("文件/夹路径为空")
        elif file_or_folder_status == 0:
            self.status.append("\n"+"开始检测文件:"+path)
            details = []
            for i in range(3):
                detail = {}
                detail["name"] = "x"+i
                detail["x"] = i*10
                detail["p"]= i+100
                details[i]=detail
            self.result_file(self.label_middle2, self.label_right2, path)
            # self.result(self.label_middle2,self.label_right1,details,path1=path)
        elif file_or_folder_status == 1:
            self.status.append("\n"+"开始检测文件夹:"+path)
            # self.showDialog("开始检测文件夹"+path)
            # self.result(self., text)
        else:
            print("文件/文件夹状态异常")
    #     加载图片槽
    def loadImage(self):
        global path
        fname, _ = QFileDialog.getOpenFileName(self, "打开文件", '.', '图像文件(*.jpg *.png)')
        path = fname
        self.label_middle1.setScaledContents(True)
        self.label_right2.setText(path)
        self.status.append("已选择 "+path+" \n请开始检测...")
        pixmap = QPixmap(fname)
        sz = QSize(self.label_middle1.width(),self.label_middle1.height())
        pixmap = pixmap.scaled(sz,Qt.KeepAspectRatio)
        self.label_middle1.setPixmap(pixmap)

    def loadPath(self):
        # 待完成
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.AnyFile)
        dlg.setFilter(QDir.Files)
    # QRadioButton事件
    def btnstate(self,btn):
        global file_or_folder_status
        if btn.text()=="文件":
            if btn.isChecked()==True:
                self.status.setText("请选择文件.....")
                # print(btn.text()+"is selected")
                file_or_folder_status = 0;
                # print(file_or_folder_status)
            # else:
                # print(btn.text()+"is not selected")

        if btn.text()=="文件夹":
            if btn.isChecked()==True:
                self.status.setText("请选择文件夹......")
                file_or_folder_status = 1;
                # print(file_or_folder_status)
                # print(btn.text()+"is selected")
            # else:
                # print(btn.text()+"is not selected")
    def showDialog(self,paramater):
        messageBox = QMessageBox()
        messageBox.warning(self,"警告!",paramater,QMessageBox.Yes,QMessageBox.Yes)
        # messageBox.show()
        # messageBox.exec_()
        # dialog = QDialog()
        # # text = QLabel(paramater, dialog)
        # btn  = QPushButton("ok", dialog)
        # dialog.setWindowTitle("错误提示")
        # dialog.setWindowModality(Qt.ApplicationModal)
        # dialog.exec_()
        # 检测结果展示
    def result_file(self, pix,text,path1):
        pixmap = QPixmap(path1)
        pix.setScaledContents(True)
        sz = QSize(pix.width(), pix.height())
        pixmap = pixmap.scaled(sz, Qt.KeepAspectRatio)
        pix.setPixmap(QPixmap(pixmap))

    def result(self,pix,text,details,path1):
        pix.setPixmap(QPixmap(path1))
        # for detail in details:
        #     text.append("名称"+detail["name"]+"\n")
        #     text.append("坐标"+detail["x"]+"\n")
        #     text.append("概率"+detail["p"]+"\n")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())