# https://github.com/baoboa/pyqt5/blob/master/examples/itemviews/spinboxdelegate.py
# https://doc.qt.io/qt-5/qtwidgets-itemviews-spinboxdelegate-example.html

from PyQt5.QtCore import QModelIndex, Qt
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtWidgets import (QApplication, QSpinBox, QStyledItemDelegate,
        QTableView)


class SpinBoxDelegate(QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        editor = QSpinBox(parent)
        editor.setFrame(False)
        editor.setMinimum(0)
        editor.setMaximum(100)

        return editor

    def setEditorData(self, spinBox, index):
        value = index.model().data(index, Qt.EditRole)

        spinBox.setValue(value)

    def setModelData(self, spinBox, model, index):
        spinBox.interpretText()
        value = spinBox.value()

        model.setData(index, value, Qt.EditRole)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)

    model = QStandardItemModel(4, 2)
    tableView = QTableView()
    tableView.setModel(model)

    delegate = SpinBoxDelegate()
    tableView.setItemDelegate(delegate)

    for row in range(4):
        for column in range(2):
            index = model.index(row, column, QModelIndex())
            model.setData(index, (row + 1) * (column + 1))

    tableView.setWindowTitle("Spin Box Delegate")
    tableView.show()
    sys.exit(app.exec_())