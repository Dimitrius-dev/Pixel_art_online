# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'screen1.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form1(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(718, 631)
        self.label_game = QtWidgets.QLabel(Form)
        self.label_game.setGeometry(QtCore.QRect(230, 160, 141, 101))
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(25)
        self.label_game.setFont(font)
        self.label_game.setObjectName("label_game")
        self.pushButton_enter = QtWidgets.QPushButton(Form)
        self.pushButton_enter.setGeometry(QtCore.QRect(240, 400, 121, 31))
        self.pushButton_enter.setObjectName("pushButton_enter")
        self.label_password = QtWidgets.QLabel(Form)
        self.label_password.setGeometry(QtCore.QRect(370, 360, 47, 13))
        self.label_password.setObjectName("label_password")
        self.label_login = QtWidgets.QLabel(Form)
        self.label_login.setGeometry(QtCore.QRect(370, 320, 47, 13))
        self.label_login.setObjectName("label_login")
        self.password_value = QtWidgets.QLineEdit(Form)
        self.password_value.setGeometry(QtCore.QRect(240, 360, 121, 20))
        self.password_value.setObjectName("password_value")
        self.login_value = QtWidgets.QLineEdit(Form)
        self.login_value.setGeometry(QtCore.QRect(240, 320, 121, 20))
        self.login_value.setObjectName("login_value")
        self.label_status = QtWidgets.QLabel(Form)
        self.label_status.setGeometry(QtCore.QRect(240, 290, 121, 20))
        self.label_status.setText("")
        self.label_status.setObjectName("label_status")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_game.setText(_translate("Form", "Pixel Art\n"
"   online"))
        self.pushButton_enter.setText(_translate("Form", "Enter"))
        self.label_password.setText(_translate("Form", "password"))
        self.label_login.setText(_translate("Form", "login"))
