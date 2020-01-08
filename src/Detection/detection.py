from PyQt5.QtWidgets import QApplication,QListWidget,QHBoxLayout,QVBoxLayout,QListWidgetItem,QTextEdit,QMessageBox,QWidget,QGridLayout,QLabel,QPushButton,QRadioButton,QFileDialog,QDialog
from PyQt5.QtGui import QIcon,QPixmap,QFont
from PyQt5.QtCore import Qt,QDir,QSize
import sys
import glob
import os

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
        self.setWindowTitle("目标检测主窗口")
        self.setWindowIcon(QIcon("./../image/excavator.ico"))
        # 第一个属性是字体（微软雅黑），第二个是大小，第三个是加粗（权重是75）
        font = QFont("Microsoft YaHei", 20, 60);
        desktop = QApplication.desktop()
        # self.setGeometry(300,300,250,150)
        self.resize(int(desktop.width()*3/4),int(desktop.height()*3/4))


        self.label_left = QListWidget()
        # sz = QSize(self.label_left.width(),self.label_left.height())
        # self.label_left.setFixedSize(sz.width(),sz.height())
        self.label_left.setWindowTitle("文件夹线下图片列表")

        self.label_middle1 = QLabel()
        self.label_middle1.setText("原图片/图片集")
        self.label_middle1.setStyleSheet("font:20pt '楷体';border-width: 1px;border-style: solid;border-color: rgb(0, 0, 0);")
        self.label_middle1.setFont(font)


        self.label_middle2 = QLabel()
        # self.label_middle2.setPixmap(QPixmap("./../image/1.jpg"))
        self.label_middle2.setFont(font)
        self.label_middle2.setStyleSheet("font:20pt '楷体';border-width: 1px;border-style: solid;border-color: rgb(0, 0, 0);")
        self.label_middle2.setText("结果图片/图片集")

        self.label_right1 = QLabel()
        self.label_right1.setFont(font)
        self.label_right1.setStyleSheet("font:20pt '楷体';border-width: 1px;border-style: solid;border-color: rgb(0, 0, 0);")
        self.label_right1.setText("目标详情")

        self.label_right2 = QLabel()
        self.label_right2.setStyleSheet("border-width: 1px;border-style: solid;border-color: rgb(0, 0, 0);")
        self.label_right2.setText("文件/文件夹路径")

        self.status = QTextEdit()
        self.status.setText("就绪")

        self.radio1 = QRadioButton("文件")
        self.radio1.setChecked(True)

        self.radio2 = QRadioButton("文件夹")

        self.select  = QPushButton("选择文件/文件夹")
        self.btn_send = QPushButton("开始检测")


        #全局布局
        mainLayout = QHBoxLayout()

        # 局部布局
        layout_left = QVBoxLayout()
        widget_left = QWidget()
        layout_middle = QVBoxLayout()
        widget_middle = QWidget()
        layout_right = QVBoxLayout()
        widget_right = QWidget()

        # 左边添加控件
        layout_left.addWidget(self.label_left)
        layout_left.addWidget(self.status)
        layout_left.setStretchFactor(self.label_left, 2)
        layout_left.setStretchFactor(self.status, 1)
        widget_left.setLayout(layout_left)

    #     中间添加控件
        layout_middle.addWidget(self.label_middle1)
        layout_middle.addWidget(self.label_middle2)
        widget_middle.setLayout(layout_middle)

    # #     右边添加控件
        layout_right.addWidget(self.label_right1)
        layout_right.setStretchFactor(self.label_right1, 10)
        layout_right.addWidget(self.label_right2)
        layout_right.setStretchFactor(self.label_right2, 1)

        # 右边两个文件/文件夹需要水平方式
        label_right_2 = QHBoxLayout()
        label_right_2.addWidget(self.radio1)
        label_right_2.addWidget(self.radio2)
        widget_temp = QWidget()
        widget_temp.setLayout(label_right_2)
        layout_right.addWidget(widget_temp)
        layout_right.setStretchFactor(widget_temp, 1)
        layout_right.addWidget(self.select)
        layout_right.setStretchFactor(self.select, 1)
        layout_right.addWidget(self.btn_send)
        layout_right.setStretchFactor(self.btn_send, 1)

        widget_right.setLayout(layout_right)

        mainLayout.addWidget(widget_left)
        mainLayout.addWidget(widget_middle)
        mainLayout.addWidget(widget_right)
        widget_left.setFixedWidth(int(self.size().width()/5))
        widget_middle.setFixedWidth(int(self.size().width()*3/5))
        widget_right.setFixedWidth(int(self.size().width()/5))
        self.setLayout(mainLayout)

    # 监听事件
    def initListener(self):
        # 左上侧文件夹下文件的点击事件
        self.label_left.itemClicked.connect(self.listItemClicked)

        # 两个radiobutton的事件
        self.radio1.toggled.connect(lambda :self.btnstate(self.radio1))
        self.radio2.toggled.connect(lambda :self.btnstate(self.radio2))

    #     添加选择文件/文件夹的标签
        self.status.setText("请选择文件.....")
        self.select.clicked.connect(self.loadImage)
    #     开始检测按钮
        self.btn_send.clicked.connect(self.startDetect)

    def listItemClicked(self,item):
        global path
        file_path = path+'/'+item.text()
        self.update_text(self.label_right2,file_path)
        self.update_display(self.label_middle1,file_path)
        # 字符串分割,然后寻找Alarm里面有没有对应的名字的文件，有就展出，没有就显示
        # todo，将txt文件的结果进行解析
        folder,fname = os.path.split(file_path)
        new_path  = folder+"/"+"ssss.txt"
        text = ""
        if not os.path.exists(new_path):
            new_path = file_path
            text = "该图片暂无目标"


        self.update_text(self.label_right1,text)
        self.update_display(self.label_middle2,new_path)
        # self.update_display(self.label_right1,get_photo_info())
    def startDetect(self):
        global file_or_folder_status
        global path
        # path = 2
        # //检测某一个文件
        if path is None:
            self.showDialog("文件/夹路径为空")
        elif file_or_folder_status == 0:
            text = "\n"+"开始检测文件:"+path
            self.add_status(self.status,text)
            # --------------------------执行检测过程-----------------------------
            details = []
            for i in range(3):
                detail = {}
                detail["name"] = "x"+str(i)
                detail["x"] = i*10
                detail["p"]= i+100
                details.append(detail)
            photo_path = path
            self.result_file(self.label_middle2, self.label_right1, photo_path,details)
            # self.result(self.label_middle2,self.label_right1,details,path1=path)
        elif file_or_folder_status == 1:
            self.status.append("\n"+"开始检测文件夹:"+path)
            # 开始检测文件夹

        else:
            print("文件/文件夹状态异常")
    #     加载图片槽
    def update_display(self,label,photo_path):
        pixmap = QPixmap(photo_path)
        # sz = QSize(self.geometry().width()/2, self.geometry().width()/2)
        sz = QSize(label.size().width(), label.size().height())
        label.setScaledContents(True)
        # print(label.width(),label.height())
        pixmap = pixmap.scaled(sz, Qt.KeepAspectRatio)
        label.setPixmap(pixmap)

    # 更新label标签，label是label名字，text是要更新的str
    def update_text(self,label,text):
        label.setText(text)

    # 添加status标签内容，status是label名字，text是要更新的str
    def add_status(self,status,text):
        status.append(text)

    # 选择图片或者文件夹
    def loadImage(self):
        global path
        global  file_or_folder_status
        if file_or_folder_status==1:
            self.loadPath()
        else:
            fname, _ = QFileDialog.getOpenFileName(self, "打开文件", '.', '图像文件(*.jpg *.png)')
            path = fname
            self.update_display(self.label_middle1,path)
            self.update_text(self.label_right2,path)
            text = "已选择 " + path + " \n请开始检测..."
            self.add_status(self.status,text)

    # 选择文件夹
    def loadPath(self):
        global path
        folder_path= QFileDialog.getExistingDirectory(self,"打开文件夹",'./')
        path = folder_path
        text = "已选择文件夹： " + folder_path + " \n请开始检测..."
        self.add_status(self.status,text)
        self.update_text(self.label_right2, folder_path)
        files = os.listdir(folder_path)
        # self.label_left.
        for file in files:
            self.label_left.addItem(file)
            # text = text + file+"\n"
        # self.label_left.setText(text)

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

    # 展示检测结果文件，更新状态图片ui，以及label
    def result_file(self, pix,text,path,details):
        self.update_display(self.label_middle2,path)
        text.setText(self.getDetails(details))


    def getDetails(self,details):
        text = ""
        # details = None
        if details is None:
            text = "这张图片没有检测到目标"
            return text
        for detail in details:
            text=text+"object"
            for key in detail.keys():
                text = text+ "\t"+key+":"+str(detail[key])+"\n"
        return text

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