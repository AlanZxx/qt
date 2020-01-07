from PyQt5.QtWidgets import QApplication,QMainWindow,QDesktopWidget
import  sys
from PyQt5.QtGui import QIcon

class MainWindow(QMainWindow):
    def __init__(self,parent = None):
        super(MainWindow, self).__init__(parent)
        self.resize(500, 400)
        self.center()
        self.statusBar().showMessage("目标检测主程序", 5000)
        self.setWindowTitle("目标检测主窗口")


    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move(int((screen.width()-size.width())/2), int((screen.height()-size.height())/2))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("./../image/1.jpg"))
    form = MainWindow()
    form.show()
    sys.exit(app.exec_())