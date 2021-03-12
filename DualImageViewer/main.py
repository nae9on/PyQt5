from PyQt5 import QtWidgets
from main_ui import Ui_imageViewer
import sys


# Make sure to extend from the same widget/window (QMainWindow in this case)
# initially used to build the UI in Qt Designer
class DualImageViewer(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # Pass all arguments so that it behaves in every way like a QMainWindow

        # Setup UI on the ImageViewer instance which is also a QMainWindow instance
        self.ui = Ui_imageViewer()
        self.ui.setupUi(self)

        # Connect signals with slots
        self.connect_signals_and_slots()

    def connect_signals_and_slots(self):
        self.ui.actionAbout.triggered.connect(self.about)
        self.ui.actionAbout_Qt.triggered.connect(QtWidgets.qApp.aboutQt)

    def about(self):
        QtWidgets.QMessageBox.about(self, "Dual Image Viewer",
                          "<p>The <b>Dual Image Viewer</b> example shows how two images "
                          "can be shown in sync such that an operation (zoom, fit to window etc.)"
                          " applied to one image is automatically applied to the other </p>")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    widget = DualImageViewer()
    widget.show()
    sys.exit(app.exec_())
