from PyQt5 import QtWidgets
import sys


class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setGeometry(0, 0, 300, 300)
        self.setWindowTitle("My Title")
        self.initialize()

    def initialize(self):
        self.label = QtWidgets.QLabel(self)  # passing window as self
        self.label.setText("My Label")
        self.label.move(50, 50)

        self.button = QtWidgets.QPushButton(self) # passing window as self
        self.button.setText("Click me")
        self.button.clicked.connect(self.clicked)

    def clicked(self):
        self.label.setText("Button pressed")
        self.update()

    def update(self):
        self.label.adjustSize()


def window():
    app = QtWidgets.QApplication(sys.argv)
    win = MyWindow()
    win.show()
    sys.exit(app.exec_())


window()




