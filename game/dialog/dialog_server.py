from PyQt5.QtWidgets import QDialog

from UI.UI_dialog_server import *


class Dialog_server(QDialog, Ui_Dialog1):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)

        self.name = ""
        self.password = ""
        self.size = ""

        self.radioButton_25.click()

    def get_name(self):
        return self.lineEdit_name.text()

    def radio_buttons(self):
        if self.radioButton_25.isChecked():
            return 25
        if self.radioButton_55.isChecked():
            return 55
        if self.radioButton_85.isChecked():
            return 85

    def get_password(self):
        return self.lineEdit_password.text()
