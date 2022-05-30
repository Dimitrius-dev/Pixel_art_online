from PyQt5.QtWidgets import QDialog

from UI.UI_dialog_password import *


class Dialog_password(QDialog, Ui_Dialog2):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)

        self.password = ""

        self.lineEdit.setEchoMode(QtWidgets.QLineEdit.Password)

    def is_correct(self, password) -> bool:
        if self.lineEdit.text() == password:
            return True
        else:
            return False
