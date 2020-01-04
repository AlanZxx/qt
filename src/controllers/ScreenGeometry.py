import sys
from PyQt5.QtWidgets import QHBoxLayout,QApplication,QWidget,QMainWindow,QPushButton

def onClick_btn():
    print("1")
    print("widget.x():=%d"%widget.x())  #窗口横坐标
    print("widget.y():=%d"%widget.y())  #窗口纵坐标
    print("widget.width():=%d"%widget.width()) #工作去宽度
    print("widget.height():=%d"%widget.height()) #工作去高度


    print("2")
    print("widget.geometry():=%d"%widget.geometry().x())  #工作去横坐标
    print("widget.geometry().y():%d"%widget.geometry().y()) #工作去纵坐标
    print("widget.geometry().width()%d"%widget.geometry().width()) #工作去宽度
    print("widget.geometry().height()%d"%widget.geometry().height()) #工作去高度


    print("3")
    print("widget.frameGeometry():=%d"%widget.frameGeometry().x())    #窗口横坐标
    print("widget.frameGeometry().y():%d"%widget.frameGeometry().y())   #窗口纵坐标
    print("widget.frameGeometry().width()%d"%widget.frameGeometry().width()) #窗口宽度
    print("widget.frameGeometry().height()%d"%widget.frameGeometry().height()) #窗口高度
app = QApplication(sys.argv)

widget = QWidget()
btn = QPushButton(widget)
btn.setText("按钮")
btn.clicked.connect(onClick_btn)

btn.move(24,53)
widget.resize(400,240)
widget.move(250,200)
widget.setWindowTitle("屏幕坐标系")
widget.show()
sys.exit(app.exec_())

