# https://stackoverflow.com/questions/25187444/pyqt-qlistwidget-custom-items
# https://stackoverflow.com/questions/49385525/adding-items-to-qlistview


import sys
from PyQt5 import QtWidgets


class CustomWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(CustomWidget, self).__init__(parent)
        self.property = QtWidgets.QLabel()
        self.value = QtWidgets.QDoubleSpinBox()
        self.horizontal_layout = QtWidgets.QHBoxLayout()
        self.horizontal_layout.addWidget(self.property, 0)
        self.horizontal_layout.addWidget(self.value, 1)
        self.setLayout(self.horizontal_layout)

    def set_property(self, text):
        self.property.setText(text)

    def set_value(self, value):
        self.value.setValue(value)

    def printme(self):
        print(self.property.text(), self.value.value())


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # Create QListWidget
        self.list = QtWidgets.QListWidget(self)

        for key, value, in [
            ('Property 1', 1),
            ('Property 2', 2),
            ('Property 3', 3)]:

            # Create CustomWidget
            widget = CustomWidget()
            widget.set_property(key)
            widget.set_value(value)

            # Create QListWidgetItem
            item = QtWidgets.QListWidgetItem(self.list)

            # Set size hint
            item.setSizeHint(widget.sizeHint())

            # Add QListWidgetItem into QListWidget
            self.list.addItem(item)
            self.list.setItemWidget(item, widget)

        self.central_widget = QtWidgets.QWidget(self)
        self.vertical_layout = QtWidgets.QVBoxLayout(self.central_widget)
        self.vertical_layout.addWidget(self.list)
        self.push_button = QtWidgets.QPushButton()
        self.push_button.setText("Push")
        self.vertical_layout.addWidget(self.push_button)

        self.setCentralWidget(self.central_widget)

        self.push_button.clicked.connect(self.print_key_value)

    def print_key_value(self):
        for row in range(self.list.count()):
            item = self.list.itemWidget(self.list.item(row))
            item.printme()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())