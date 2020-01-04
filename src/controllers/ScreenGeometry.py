import sys
from PyQt5.QtWidgets import QHBoxLayout,QApplication,QWidget,QMainWindow,QPushButton

def onClick_btn():
    print("1")
    print("widget.x():=%d"%widget.x())
    print("widget.y():=%d"%widget.y())
    print("widget.width():=%d"%widget.width())
    print("widget.height():=%d"%widget.height())


    print("2")
    print("widget.geometry():=%d"%widget.geometry().x())
    print("widget.geometry().y():%d"%widget.geometry().y())
    print("widget.geometry().width()%d"%widget.geometry().width())
    print("widget.geometry().height()%d"%widget.geometry().height())


    print("3")
    print("widget.frameGeometry():=%d"%widget.frameGeometry().x())
    print("widget.frameGeometry().y():%d"%widget.frameGeometry().y())
    print("widget.frameGeometry().width()%d"%widget.frameGeometry().width())
    print("widget.frameGeometry().height()%d"%widget.frameGeometry().height())
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

