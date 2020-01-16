from PyQt5.QtWidgets import QApplication,QListWidget,QHBoxLayout,QVBoxLayout,QListWidgetItem,QTextEdit,QMessageBox,QWidget,QGridLayout,QLabel,QPushButton,QRadioButton,QFileDialog,QDialog
from PyQt5.QtGui import QIcon,QPixmap,QFont
from PyQt5.QtCore import Qt,QSize
import sys
import os
import cv2
import platform
import requests
import re
import json
import piexif

from src.Detection.config import request_url

# 0表示文件,1表示文件夹
global file_or_folder_status
global folder_path
global file_path
folder_path = None
file_path = None
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

        self.label_left_folder = QLabel()
        self.label_left_folder.setStyleSheet("border-width: 1px;border-style: solid;border-color: rgb(0, 0, 0);")
        self.label_left_folder.setText("文件夹路径")

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

        self.label_right1 = QTextEdit()
        # self.label_right1.setFont(font)
        # self.label_right1.setStyleSheet("font:20pt '楷体';border-width: 1px;border-style: solid;border-color: rgb(0, 0, 0);")
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
        layout_left.addWidget(self.label_left_folder)
        layout_left.addWidget(self.label_left)
        layout_left.addWidget(self.status)
        layout_left.setStretchFactor(self.label_left_folder, 1)
        layout_left.setStretchFactor(self.label_left, 6)
        layout_left.setStretchFactor(self.status, 3)
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
        global folder_path
        global file_path
        file_path = folder_path+'/'+item.text()
        self.update_text(self.label_right2,file_path)
        self.update_display(self.label_middle1,file_path)
        # 字符串分割,然后寻找Alarm里面有没有对应的名字的文件，有就展出，没有就显示
        # todo，将txt文件的结果进行解析
        # folder,fname = os.path.split(file_path)
        # new_path  = folder+"/"+"ssss.txt"
        # text = ""
        # if not os.path.exists(new_path):
        #     new_path = file_path
        #     text = "该图片暂无目标"
        #
        #
        # self.update_text(self.label_right1,text)
        # self.update_display(self.label_middle2,new_path)
        # self.update_display(self.label_right1,get_photo_info())
    def startDetect(self):
        global file_or_folder_status
        global file_path
        global folder_path
        # path = 2
        # //检测某一个文件
        if file_path is None or not os.path.exists(file_path):
            self.showDialog("文件/夹路径为空")
        elif file_or_folder_status == 0 or file_or_folder_status==1:
            text = "\n"+"开始检测文件:"+file_path
            self.add_status(self.status,text)
            # --------------------------执行检测过程假数据-----------------------------
            # details = []
            # for i in range(3):
            #     detail = {}
            #     detail["name"] = "x"+str(i)
            #     detail["x"] = i*10
            #     detail["p"]= i+100
            #     details.append(detail)
            # --------------------------执行检测过程 requests数据-----------------------------
            self.uploadfile(file_path)
        elif file_or_folder_status == 1:
            self.status.append("\n"+"开始检测文件夹:"+folder_path)
            # 开始检测文件夹
        else:
            print("文件/文件夹状态异常")

    def uploadfile(self,file):
        uploadfile = {'file': open(file, 'rb')}
        response = requests.post(request_url.last_url,files = uploadfile)
        # 请求成功.
        if response.status_code==200:
            # 进行画图操作
            # print(response.text)
            self.draw_img(response.text)
        # 请求失败
        elif response.status_code==500:
            self.showDialog("请求失败")
        else:
            self.showDialog("返回值异常")

    def draw_img(self, text):
        global file_path
        # text格式为["msg":""]
        result = json.loads(text)
        # print("result",result)
        temp = result["msg"].split(": Predicted")
        print(temp)
        file_path = file_path
        # print(file_path)
        # get each image obj 使用“.\n”进行分割
        obj_split = re.split(r'\.\n', temp[1])
        print(obj_split)
        if (len(obj_split) <= 1):
            self.showDialog("图片里未检测出目标")
            print("there has no objs!")
            return
        # print("obj_split: "+str(obj_split))
        objs = re.split(r'\n', obj_split[1])
        # print("objs: "+str(objs))
        ob = []
        for i in range(len(objs)):
            # self.update_text(self.label_right1,str(objs))
            print("add the label %d/%d......................." % (i + 1, len(objs)))
            ob.append(objs[i])
            # print(objs[i])
        if (len(ob) >= 1):
            print("plot objs use strings......")
            new_path,objs = self.plot_rectangle(file_path, ob)
            print("new_path:",new_path)
            if new_path is  not None:
                self.update_display(self.label_middle2,new_path)
                obj = self.get_objs(objs)
                self.update_text(self.label_right1,str(obj))
                self.showDialog("检测完成!")
                self.add_status(self.status,"检测完成!")
        else:
            self.showDialog("图片里无目标")
            print("there has no obs!............................")
        return
    def get_objs(self,objs):
        obj = ""
        obj = obj+"总目标数:"+str(objs["counts"])+":\n"
        for ob in objs["obj"]:
            # obj=obj+ob["name"]
            # plot_data["counts"]=plot_data["counts"]+1
            # new_obj['name']=name
            # new_obj["x"]=x
            # new_obj["y"]=y
            # new_obj["width"]=width
            # new_obj["height"]=height
            # new_obj["faith"]=faith
            obj = obj+"目标名称："+str(ob['name'])+"\t"+ \
                  "x:"+str(ob['x'])+"\t"+\
                  "y:"+str(ob['y'])+"\t" +\
                  "width:"+str(ob['width'])+"\t"+\
                  "height:"+str(ob['height'])+"\t" +\
                  "可信度:"+str(ob['faith'])+"\n"+"\n"
        return obj


    def plot_rectangle(self,img_path, objs):
        alarm_path_name = "ImageAlarm"
        error_path_name = "ImageError"
        img_path = img_path.strip()
        print("img_path--------:", img_path)
        fileIsExist = os.path.exists(img_path)

        # windows:
        print(platform.system())
        if platform.system() == "Windows":
            path_list = os.path.split(img_path)
            # alarm_path = os.path.join(os.path.split(path_list[0])[0], alarm_path_name)
            # error_path = os.path.join(os.path.split(path_list[0])[0], error_path_name)
        # Linux
        elif platform.system() == "Linux":
            path_list = img_path.split("/")
            # print(path_list)
            # error_path = "/".join(path_list[0:-2]) + "/" + error_path_name + "/"
            # alarm_path = "/".join(path_list[0:-2]) + "/" + alarm_path_name + "/"

        if (not fileIsExist):
            self.showDialog("plot_img_path is invalid!")
            print("plot_img_path is invalid!")
            return
        if len(objs) == 0:
            print("-------------------It has no obj!-----------")
            return
        img = cv2.imread(img_path, cv2.IMREAD_COLOR)

        # h = img.shape[0]
        # w = img.shape[1]
        # print(h, w)
        # plot rectangle
        print("plot rectange labels.....---------------------------------------")
        plot_data ={}
        plot_data["counts"]=0
        new_objs=[]
        for obj in objs:
            new_obj = {}
            print("label info:" + obj)
            mm = obj.split(":")
            if (len(mm) != 6):
                # self.showDialog("检测结果有异常部分!")
                print('error path length is error ,add add to error folder')
                # # error_path ="/".join(path_list[0:-2]) + "/" + "ImageError" + "/"
                # # #error_path = "/".join(paths[0:-2])+"/"+"error"
                # if not os.path.exists(error_path):
                #     os.makedirs(error_path)
                # temp = open(os.path.join(error_path, "error_path.txt"), "w")
                # temp.write(img_path + "\n")
                # temp.close()
                continue
            # print(mm)
            name = mm[0].strip()
            faith = str(mm[1].split("%")[0]).strip()
            x = int(str(mm[2].split("t")[0]).strip())
            y = int(str(mm[3].split("w")[0]).strip())
            width = int(str(mm[4].split("h")[0]).strip())
            height = int(str(mm[5].split(")")[0]).strip())
            plot_data["counts"]=plot_data["counts"]+1
            new_obj['name']=name
            new_obj["x"]=x
            new_obj["y"]=y
            new_obj["width"]=width
            new_obj["height"]=height
            new_obj["faith"]=faith
            new_objs.append(new_obj)
            # # width = int(width/2)
            # highth = 95
            # # highth = int(highth/2)
            # points = []
            # # print(np.asarray((x-width, y-highth), dtype=int))
            cv2.rectangle(img, (x, y), (x + width, y + height), (0, 0, 255), 5)
            text = name
            font = cv2.FONT_HERSHEY_COMPLEX
            plot_x = x
            plot_y = y - 7
            if (y - 7 < 45):
                plot_y = y + height + 45
            cv2.putText(img, text, (plot_x, plot_y), font, 2, (0, 0, 255), 5)
            print('plot success')

        plot_data["obj"] =new_objs
        new_img_name = "new_"+path_list[-1]
        file_path = path_list[0]
        # img_name = "sss.jpg"
        # print("name:" + img_name)
        # alarm_path = "/".join(path_list[0:-2]) + "/" + "ImageAlarm" + "/"
        # print(alarm_path)
        # if not os.path.exists(alarm_path):
        #     # create_alarmpath = "sudo mkdir"
        #     # os.system(create_alarmpath)
        #     os.makedirs(alarm_path)
        cv2.imwrite(os.path.join(file_path, new_img_name), img)
        # os.chmod(os.path.join(alarm_path, img_name), stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)  # 赋予alarm图片文件777权限

        try:
            piexif.transplant(img_path, os.path.join(file_path, new_img_name))
        except ValueError:
            print("图片%s没有GPS信息" % img_path)
        print('plot total success!---------------')
        return file_path+"/"+new_img_name,plot_data
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
        global file_path
        global folder_path
        global  file_or_folder_status
        # 打开文件夹
        if file_or_folder_status==1:
            self.loadPath()
        else:
            fname, _ = QFileDialog.getOpenFileName(self, "打开文件", '.', '图像文件(*.jpg *.png)')
            file_path = fname
            self.update_display(self.label_middle1,file_path)
            self.update_text(self.label_right2,file_path)
            text = "已选择 " + file_path + " \n请开始检测..."
            self.add_status(self.status,text)

    # 选择文件夹
    def loadPath(self):
        global folder_path
        folder_path_select= QFileDialog.getExistingDirectory(self,"打开文件夹",'./')
        folder_path = folder_path_select
        self.label_left_folder.setText("当前文件夹："+folder_path_select)
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
        self.update_display(pix,path)
        text.setText(str(details))
        # text.setText(self.getDetails(details))


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