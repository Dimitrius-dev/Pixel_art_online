from PyQt5.QtWidgets import QMessageBox

from UI.UI_screen2 import Ui_Form2
from dialog.dialog_password import *
from dialog.dialog_server import Dialog_server

from screen.screen3 import *

import json


class Menu(QMainWindow, Ui_Form2):
    def __init__(self, parent):
        super(Menu, self).__init__()
        self.setupUi(self)

        self.setWindowTitle("Пиксель Арт")

        self.parent = parent
        self.client = parent.client

        self.listWidget.setSpacing(10)

        self.servers = []

        self.next_screen = None

        self.cur_server = ""
        self.cur_password = ""
        self.cur_x = 0
        self.cur_y = 0

        self.listWidget.itemClicked.connect(self.clicked_on_item)

        self.pushButton_create.clicked.connect(self.create)
        self.pushButton_update.clicked.connect(self.update)
        self.pushButton_delete.clicked.connect(self.delete)
        self.pushButton_join.clicked.connect(self.join)

        self.update()

    def clicked_on_item(self, item):
        print(item.text())

        self.cur_server = item.text()

    def update(self):
        try:
            dict_resp = {}
            dict_resp['mode'] = "GET_SERVERS"
            self.client.do_send(str(dict_resp))

            dict_f = self.client.do_read()
            print(f"server: {dict_f}")
            dict_f = dict_f.replace('\'', "\"")
            dict_f = json.loads(dict_f)

            self.listWidget.clear()

            for d in dict_f['list']:
                # print(dict_f['list'][d])
                self.listWidget.addItem(dict_f['list'][d])

            return True
        except Exception as ex:
            print(ex)
            self.to_authoriz()
            return False

    def create(self):
        if not self.update():
            return

        dict_resp = {}
        size = ""

        dlg_server = Dialog_server()
        if not dlg_server.exec_():
            msg = QMessageBox(self)
            msg.setWindowTitle("ошибка")
            msg.setText("попробуйте снова")
            x = msg.exec_()
            return

        dict_resp['name'] = dlg_server.get_name()
        dict_resp['password'] = dlg_server.get_password()
        size = str(dlg_server.radio_buttons())

        dict_resp['mode'] = "CREATE"
        dict_resp['x'] = size
        dict_resp['y'] = size
        dict_resp['data'] = "12345"
        self.client.do_send(str(dict_resp))

        self.update()

    def delete(self):
        if not self.update():
            return

        if not self.check_password():
            return

        dict_resp = {}
        dict_resp['mode'] = "DELETE"
        dict_resp['name'] = self.cur_server
        self.client.do_send(str(dict_resp))

        self.update()

    def to_authoriz(self):
        self.parent.show()
        self.hide()

    def update_elem_by_name(self):
        dict_resp = {}
        dict_resp['mode'] = "GET_SERVER"
        dict_resp['name'] = self.cur_server
        self.client.do_send(str(dict_resp))

        dict_f = self.client.do_read()
        # print(f"server: {dict_f}")
        dict_f = dict_f.replace('\'', "\"")
        dict_f = json.loads(dict_f)

        if dict_f['mode'] != "ERROR":
            self.cur_x = int(dict_f['x'])
            self.cur_y = int(dict_f['y'])
            self.cur_password = dict_f['password']
            return True
        return False

    def check_password(self):
        if not self.update():
            return

        if not self.update_elem_by_name():
            return False

        dlg_password = Dialog_password()
        if not dlg_password.exec_():
            return False
        if not dlg_password.is_correct(self.cur_password):
            msg = QMessageBox(self)
            msg.setWindowTitle("password")
            msg.setText("Wrong password")
            x = msg.exec_()
            return False
        return True


    def join(self):
        try:
            self.update()

            if not self.check_password():
                return

            self.next_screen = Paint(self, self.cur_server, self.cur_x, self.cur_y)

            self.next_screen.show()

            self.hide()

        except Exception as ex:
            print(ex)




