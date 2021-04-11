# https://stackoverflow.com/questions/25187444/pyqt-qlistwidget-custom-items

import sys
from PyQt5 import QtGui, QtWidgets


class CustomWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.vertical_layout = QtWidgets.QVBoxLayout()
        self.text_up_label = QtWidgets.QLabel()
        self.text_down_label = QtWidgets.QLabel()
        self.vertical_layout.addWidget(self.text_up_label)
        self.vertical_layout.addWidget(self.text_down_label)

        self.horizontal_layout = QtWidgets.QHBoxLayout()
        self.icon_label = QtWidgets.QLabel()
        self.horizontal_layout.addWidget(self.icon_label, 0)
        self.horizontal_layout.addLayout(self.vertical_layout, 1)
        self.setLayout(self.horizontal_layout)

        # setStyleSheet
        self.text_up_label.setStyleSheet('''
            color: rgb(0, 0, 255);
        ''')
        self.text_down_label.setStyleSheet('''
            color: rgb(255, 0, 0);
        ''')

    def set_text_up(self, text):
        self.text_up_label.setText(text)

    def set_text_down(self, text):
        self.text_down_label.setText(text)

    def set_icon(self, image_path):
        self.icon_label.setPixmap(QtGui.QPixmap(image_path))


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # Create QListWidget
        self.list = QtWidgets.QListWidget(self)

        for index, name, icon in [
            ('No.1', 'Meyoko', 'icon.jpg'),
            ('No.2', 'Nyaruko', 'icon.jpg'),
            ('No.3', 'Louise', 'icon.jpg')]:

            # Create CustomWidget
            widget = CustomWidget()
            widget.set_text_up(index)
            widget.set_text_down(name)
            widget.set_icon(icon)

            # Create QListWidgetItem
            item = QtWidgets.QListWidgetItem(self.list)

            # Set size hint
            item.setSizeHint(widget.sizeHint())

            # Add QListWidgetItem into QListWidget
            self.list.addItem(item)
            self.list.setItemWidget(item, widget)

        self.setCentralWidget(self.list)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())