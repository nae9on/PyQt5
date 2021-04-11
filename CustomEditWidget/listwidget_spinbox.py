# https://stackoverflow.com/questions/25187444/pyqt-qlistwidget-custom-items
# https://stackoverflow.com/questions/49385525/adding-items-to-qlistview


import sys
from PyQt5 import QtWidgets
import numpy as np


class IntWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.property = QtWidgets.QLabel()
        self.property.setFixedWidth(50)
        self.value = QtWidgets.QSpinBox()
        self.value.setMinimum(np.iinfo(np.int32).min)
        self.value.setMaximum(np.iinfo(np.int32).max)
        self.horizontal_layout = QtWidgets.QHBoxLayout()
        self.horizontal_layout.addWidget(self.property, 0)
        self.horizontal_layout.addWidget(self.value, 1)
        self.setLayout(self.horizontal_layout)

    def set_property(self, text):
        self.property.setText(text)

    def set_value(self, value):
        self.value.setValue(value)

    def get_key_value(self):
        return self.property.text(), self.value.value()


class FloatWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.property = QtWidgets.QLabel()
        self.property.setFixedWidth(50)
        self.value = QtWidgets.QDoubleSpinBox()
        self.value.setMinimum(np.finfo(np.float32).min)
        self.value.setMaximum(np.finfo(np.float32).max)
        self.value.setDecimals(6)
        self.horizontal_layout = QtWidgets.QHBoxLayout()
        self.horizontal_layout.addWidget(self.property, 0)
        self.horizontal_layout.addWidget(self.value, 1)
        self.setLayout(self.horizontal_layout)

    def set_property(self, text):
        self.property.setText(text)

    def set_value(self, value):
        self.value.setValue(value)

    def get_key_value(self):
        return self.property.text(), self.value.value()


class StringWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.property = QtWidgets.QLabel()
        self.property.setFixedWidth(50)
        self.value = QtWidgets.QLineEdit()
        self.horizontal_layout = QtWidgets.QHBoxLayout()
        self.horizontal_layout.addWidget(self.property, 0)
        self.horizontal_layout.addWidget(self.value, 1)
        self.setLayout(self.horizontal_layout)

    def set_property(self, text):
        self.property.setText(text)

    def set_value(self, value):
        self.value.setText(value)

    def get_key_value(self):
        return self.property.text(), self.value.text()


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # Create QListWidget
        self.list = QtWidgets.QListWidget(self)

        for key, value, in [
            ('Integer', 1),
            ('Float', 2.0),
            ('String', 'Red')]:

            # Create IntWidget
            if isinstance(value, int):
                widget = IntWidget()
            elif isinstance(value, float):
                widget = FloatWidget()
            elif isinstance(value, str):
                widget = StringWidget()

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

        self.setWindowTitle('Editor')

        self.push_button.clicked.connect(self.print_key_value)

    def print_key_value(self):
        for row in range(self.list.count()):
            item = self.list.itemWidget(self.list.item(row))
            key, value = item.get_key_value()
            print(key, value)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
