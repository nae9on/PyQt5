from PyQt5 import QtWidgets, QtGui
from main_ui import Ui_MainWindow
import sys


# Make sure to extend from the same widget/window (QMainWindow in this case)
# initially used to build the UI in Qt Designer
class DualImageViewer(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # Pass all arguments so that it behaves in every way like a QMainWindow

        # Setup UI on the ImageViewer instance which is also a QMainWindow instance
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Connect signals with slots
        self.connect_signals_and_slots()

    def connect_signals_and_slots(self):
        self.ui.actionOpen_Image.triggered.connect(self.open)
        self.ui.actionAbout.triggered.connect(self.about)
        self.ui.actionAbout_Qt.triggered.connect(QtWidgets.qApp.aboutQt)

    def about(self):
        QtWidgets.QMessageBox.about(self, "Dual Image Viewer",
                          "<p>The <b>Dual Image Viewer</b> example shows how two images "
                          "can be shown in sync such that an operation (zoom, fit to window etc.)"
                          " applied to one image is automatically applied to the other </p>")

    def open(self):
        options = QtWidgets.QFileDialog.Options()
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'QFileDialog.getOpenFileName()', '',
                                                  'Images (*.png *.jpeg *.jpg *.bmp *.gif)', options=options)
        if file_name:
            print(file_name)
            image = QtGui.QImage(file_name)
            if image.isNull():
                QtWidgets.QMessageBox.information(self, "Dual Image Viewer", "Cannot load %s." % file_name)
                return

            self.ui.imageLabelLeft.setPixmap(QtGui.QPixmap.fromImage(image))
            self.ui.imageLabelLeft.setBackgroundRole(QtGui.QPalette.Base)
            self.scaleFactor = 1.0

            self.ui.scrollAreaLeft.setVisible(True)
            self.ui.actionFit_to_Window.setEnabled(True)
            self.update_actions()

            if not self.ui.actionFit_to_Window.isChecked():
                self.ui.imageLabelLeft.adjustSize()

    def update_actions(self):
        self.ui.actionZoom_In.setEnabled(not self.ui.actionFit_to_Window.isChecked())
        self.ui.actionZoom_Out.setEnabled(not self.ui.actionFit_to_Window.isChecked())
        self.ui.actionNormal_Size.setEnabled(not self.ui.actionFit_to_Window.isChecked())


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    widget = DualImageViewer()
    widget.show()
    sys.exit(app.exec_())
