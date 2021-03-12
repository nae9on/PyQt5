# Reference https://github.com/baoboa/pyqt5/blob/master/examples/widgets/imageviewer.py

from PyQt5 import QtCore, QtWidgets, QtGui, QtPrintSupport
import sys


class QImageViewer(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # Add a printer
        self.printer = QtPrintSupport.QPrinter()
        self.scaleFactor = 0.0

        # Create a label to display an image (has the ability to scale images)
        self.imageLabel = QtWidgets.QLabel()
        self.imageLabel.setBackgroundRole(QtGui.QPalette.Base)
        # Set size policy to "Ignored" making the users able to scale the image to whatever
        # size they want when the "Fit to Window" option is turned on. Otherwise, the default
        # size policy "preferred" will make scroll bars appear when the scroll area becomes
        # smaller than the label's minimum size hint.
        self.imageLabel.setSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
        # To make sure that the image is zoomed when the QLabel is zoomed
        self.imageLabel.setScaledContents(True)

        # Create the scroll area
        # Preserve the focal point after scaling an image.
        self.scrollArea = QtWidgets.QScrollArea()
        self.scrollArea.setBackgroundRole(QtGui.QPalette.Dark)
        # Make imageLabel the scroll area's child widget,
        self.scrollArea.setWidget(self.imageLabel)
        self.scrollArea.setVisible(False)

        # Make scrollArea the central widget of the QMainWindow.
        self.setCentralWidget(self.scrollArea)

        # Construct widget
        self.create_actions()
        self.create_menus()

        self.setWindowTitle("Image Viewer")
        self.resize(800, 600)

    # slot
    def open(self):
        options = QtWidgets.QFileDialog.Options()
        # file_name = QFileDialog.getOpenFileName(self, "Open File", QDir.currentPath())
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'QFileDialog.getOpenFileName()', '',
                                                             "Images (*.png *.jpeg *.jpg *.bmp *.gif)", options=options)
        if file_name:
            image = QtGui.QImage(file_name)
            if image.isNull():
                # use a QMessageBox to alert the user.
                QtWidgets.QMessageBox.information(self, "Image Viewer", "Cannot load %s." % file_name)
                return

            # Display the image in imageLabel by setting the label's pixmap.
            self.imageLabel.setPixmap(QtGui.QPixmap.fromImage(image))
            self.scaleFactor = 1.0

            self.scrollArea.setVisible(True)
            self.printAct.setEnabled(True)
            self.fitToWindowAct.setEnabled(True)
            self.update_actions()

            if not self.fitToWindowAct.isChecked():
                self.imageLabel.adjustSize()

    # slot
    def print_(self):
        dialog = QtPrintSupport.QPrintDialog(self.printer, self)
        if dialog.exec_():
            painter = QtGui.QPainter(self.printer)
            rect = painter.viewport()
            size = self.imageLabel.pixmap().size()
            size.scale(rect.size(), QtCore.Qt.KeepAspectRatio)
            painter.setViewport(rect.x(), rect.y(), size.width(), size.height())
            painter.setWindow(self.imageLabel.pixmap().rect())
            painter.drawPixmap(0, 0, self.imageLabel.pixmap())

    # slot
    def zoom_in(self):
        self.scale_image(1.25)

    # slot
    def zoom_out(self):
        self.scale_image(0.8)  # Note 1.25 * 0.8 = 1

    # slot
    def normal_size(self):
        # Restore the normal size of the currently displayed image
        self.imageLabel.adjustSize()
        # Reset the scale factor to 1
        self.scaleFactor = 1.0

    # slot
    def fit_to_window(self):
        fit_to_window = self.fitToWindowAct.isChecked()
        # Make scroll area to resize its child widget
        self.scrollArea.setWidgetResizable(fit_to_window)
        if not fit_to_window:
            self.normal_size()

        # Disable the Zoom In, Zoom Out and Normal Size menu entries
        self.update_actions()

    # slot
    def about(self):
        QtWidgets.QMessageBox.about(self, "About Image Viewer",
                          "<p>The <b>Image Viewer</b> example shows how to combine "
                          "QLabel and QScrollArea to display an image. QLabel is "
                          "typically used for displaying text, but it can also display "
                          "an image. QScrollArea provides a scrolling view around "
                          "another widget. If the child widget exceeds the size of the "
                          "frame, QScrollArea automatically provides scroll bars.</p>"
                          "<p>The example demonstrates how QLabel's ability to scale "
                          "its contents (QLabel.scaledContents), and QScrollArea's "
                          "ability to automatically resize its contents "
                          "(QScrollArea.widgetResizable), can be used to implement "
                          "zooming and scaling features.</p>"
                          "<p>In addition the example shows how to use QPainter to "
                          "print an image.</p>")

    def create_actions(self):
        self.openAct = QtWidgets.QAction("&Open...", self, shortcut="Ctrl+O", triggered=self.open)
        self.printAct = QtWidgets.QAction("&Print...", self, shortcut="Ctrl+P", enabled=False, triggered=self.print_)
        self.exitAct = QtWidgets.QAction("E&xit", self, shortcut="Ctrl+Q", triggered=self.close)
        self.zoomInAct = QtWidgets.QAction("Zoom &In (25%)", self, shortcut="Ctrl++", enabled=False, triggered=self.zoom_in)
        self.zoomOutAct = QtWidgets.QAction("Zoom &Out (25%)", self, shortcut="Ctrl+-", enabled=False, triggered=self.zoom_out)
        self.normalSizeAct = QtWidgets.QAction("&Normal Size", self, shortcut="Ctrl+S", enabled=False, triggered=self.normal_size)
        self.fitToWindowAct = QtWidgets.QAction("&Fit to Window", self, enabled=False, checkable=True, shortcut="Ctrl+F",
                                                triggered=self.fit_to_window)
        self.aboutAct = QtWidgets.QAction("&About", self, triggered=self.about)
        self.aboutQtAct = QtWidgets.QAction("About &Qt", self, triggered=QtWidgets.qApp.aboutQt)

    def create_menus(self):
        # Create File menu
        self.fileMenu = QtWidgets.QMenu("&File", self)
        self.fileMenu.addAction(self.openAct)
        self.fileMenu.addAction(self.printAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.exitAct)

        # Create View menu
        self.viewMenu = QtWidgets.QMenu("&View", self)
        self.viewMenu.addAction(self.zoomInAct)
        self.viewMenu.addAction(self.zoomOutAct)
        self.viewMenu.addAction(self.normalSizeAct)
        self.viewMenu.addSeparator()
        self.viewMenu.addAction(self.fitToWindowAct)

        # Create Help menu
        self.helpMenu = QtWidgets.QMenu("&Help", self)
        self.helpMenu.addAction(self.aboutAct)
        self.helpMenu.addAction(self.aboutQtAct)

        # Set the created menu's as sub-menu's under the Main menu
        self.menuBar().addMenu(self.fileMenu)
        self.menuBar().addMenu(self.viewMenu)
        self.menuBar().addMenu(self.helpMenu)

    # Enables or disables the Zoom In, Zoom Out and Normal Size menu entries depending on whether the Fit to Window
    # option is turned on or off.
    def update_actions(self):
        self.zoomInAct.setEnabled(not self.fitToWindowAct.isChecked())
        self.zoomOutAct.setEnabled(not self.fitToWindowAct.isChecked())
        self.normalSizeAct.setEnabled(not self.fitToWindowAct.isChecked())

    # Use the factor parameter to calculate the new scaling factor for the displayed image, and resize imageLabel.
    def scale_image(self, factor):
        self.scaleFactor *= factor
        self.imageLabel.resize(self.scaleFactor * self.imageLabel.pixmap().size())

        # adjust the scroll bars to preserve the focal point of the image.
        self.adjust_scroll_bar(self.scrollArea.horizontalScrollBar(), factor)
        self.adjust_scroll_bar(self.scrollArea.verticalScrollBar(), factor)

        # Disable menu entries when system limits are exceeding
        self.zoomInAct.setEnabled(self.scaleFactor < 3.0)
        self.zoomOutAct.setEnabled(self.scaleFactor > 0.333)

    # Whenever we zoom in or out, we need to adjust the scroll bars in consequence.
    @staticmethod
    def adjust_scroll_bar(scroll_bar, factor):
        scroll_bar.setValue(int(factor * scroll_bar.value()
                                + ((factor - 1) * scroll_bar.pageStep() / 2)))


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    image_viewer = QImageViewer()
    image_viewer.show()
    sys.exit(app.exec_())
