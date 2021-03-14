from PyQt5 import QtWidgets, QtGui
from main_ui import Ui_MainWindow
from authentication import Authenticator
from login_exceptions import UsernameAlreadyExists, PasswordTooWeak, InvalidUsername, InvalidPassword
import sys


class LoginSystem(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.authenticator = Authenticator()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.connect_signals_and_slots()

    def connect_signals_and_slots(self):
        self.ui.pushButton.clicked.connect(self.sign_in)
        self.ui.pushButton_2.clicked.connect(self.agree_and_join)

    def sign_in(self):
        popup_window = QtWidgets.QMessageBox()
        popup_window.setWindowTitle("Message")
        if self.authenticator.is_logged_in(self.ui.lineEdit.text()):
            popup_window.setIcon(QtWidgets.QMessageBox.Information)
            popup_window.setText("Already logged in")
            popup_window.exec()
        else:
            try:
                self.authenticator.login(self.ui.lineEdit.text(), self.ui.lineEdit_2.text())
                popup_window.setIcon(QtWidgets.QMessageBox.Information)
                popup_window.setText("Login successful")
            except InvalidUsername:
                popup_window.setIcon(QtWidgets.QMessageBox.Critical)
                popup_window.setText("User does not exist")
            except InvalidPassword:
                popup_window.setIcon(QtWidgets.QMessageBox.Critical)
                popup_window.setText("Invalid password")
            finally:
                popup_window.exec()

    def agree_and_join(self):
        popup_window = QtWidgets.QMessageBox()
        popup_window.setWindowTitle("Message")

        # popup_window.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
        # return_value = popup_window.exec()
        # if return_value == QtWidgets.QMessageBox.Ok:
        #     print('OK clicked')

        try:
            self.authenticator.add_user(self.ui.lineEdit_3.text(), self.ui.lineEdit_4.text())
        except UsernameAlreadyExists:
            popup_window.setIcon(QtWidgets.QMessageBox.Critical)
            popup_window.setText("Username already exists")
        except PasswordTooWeak:
            popup_window.setIcon(QtWidgets.QMessageBox.Critical)
            popup_window.setText("Password is too weak")
        else:
            popup_window.setIcon(QtWidgets.QMessageBox.Information)
            popup_window.setText("Username added")
        finally:
            popup_window.exec()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    widget = LoginSystem()
    widget.show()
    sys.exit(app.exec_())

    #authenticator = Authenticator()
    #authenticator.add_user("X", "Xpassword")
    #authenticator.login("X", "Xpassword")
    #print(authenticator.is_logged_in("X"))
