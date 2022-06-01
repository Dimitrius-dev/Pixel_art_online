# utf-8 is not supported

from UI.UI_screen1 import Ui_Form1
from network.SQLtool import SQL
from network.network import Network
from screen.screen2 import *

from config import host_server, port_server


class Authoriz(QMainWindow, Ui_Form1):
    def __init__(self):
        super(Authoriz, self).__init__()
        self.setupUi(self)
        self.setMouseTracking(True)

        self.setWindowTitle("Пиксель Арт")

        self.next_screen = None

        self.server_ip = host_server
        self.server_port = port_server

        # BUTTONS
        self.pushButton_enter.clicked.connect(self.check)

        # client-----------------
        self.msg = ""

        self.msg_size = 6
        self.timeout_read = 120  # seconds
        self.timeout_conn = 1  # seconds

        self.client = None
        # self.client.create(self.msg_size, self.timeout_read, self.timeout_conn)

        self.sql_tool = SQL()

        self.password_value.setEchoMode(QtWidgets.QLineEdit.Password)

        pass

    def reset(self):
        self.next_screen = None
        self.label_status.setText("")

    def check(self):
        self.client = Network()
        self.client.create(self.msg_size, self.timeout_read, self.timeout_conn)

        if not self.sql_tool.is_password(self.login_value.text(), self.password_value.text()):
            self.label_status.setText("доступ заблокирован(БД)")
            print("enter blocked")
            return
        else:
            print("entered success1")

        self.client.set_address(self.server_ip, self.server_port)
        if self.client.start():
            print("entered success2")
        else:
            self.label_status.setText("доступ заблокирован(сервер)")
            print("enter blocked")
            return

        self.to_screen_2()

    def to_screen_2(self):

        self.next_screen = Menu(self)
        self.next_screen.show()

        self.hide()


