from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
import sys


class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setGeometry(0, 0, 400, 200)
        self.setWindowTitle("Switch")
        self.label = None
        self.button = None
        self.initialize()

    def initialize(self):
        # Create label
        self.label = QtWidgets.QLabel(self)  # passing window as self
        self.label.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("QLabel {background-color: red;}")
        self.label.setText("OFF")
        # self.label.move(200, 100)
        self.label.setGeometry(200, 100, 25, 25)

        # Create button
        self.button = QtWidgets.QPushButton(self) # passing window as self
        self.button.setText("ON/OFF")
        self.button.setGeometry(100, 100, 100, 25)
        # clicked signal
        self.button.clicked.connect(self.clicked)

    # slot
    def clicked(self):
        if self.label.text() == "OFF":
            self.label.setText("ON")
        else:
            self.label.setText("OFF")
        self.update()

    def update(self):
        pass
        # self.label.adjustSize()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = MyWindow()
    main_window.show()
    sys.exit(app.exec_())