import threading

from PyQt5.QtGui import QPixmap, QPainter, QPen
from PyQt5.QtWidgets import QColorDialog, QMainWindow, QFileDialog

from UI.UI_screen3 import *

import json

import traceback


class Paint(QMainWindow, Ui_Form3):
    update_graphic_view = pyqtSignal()

    def __init__(self, parent, name, screen_x, screen_y):
        super(Paint, self).__init__()
        self.setupUi(self)

        self.setWindowTitle("Пиксель Арт")

        self.parent = parent
        self.client = parent.client

        self.name = name
        self.screen_x = screen_x
        self.screen_y = screen_y

        self.my_thread = None

        self.msg_json = ""

        # CONNECT SLOTS
        self.update_graphic_view.connect(self.update)
        self.graphicsView.scene.clicked.connect(self.mouse_update)

        self.screen_pixmap = QPixmap(self.screen_x, self.screen_y)
        self.screen_pixmap.fill(QColor(255, 255, 255))

        self.color_pixmap = QPixmap(41, 41)
        self.color_pixmap.fill(QColor(0, 0, 0))
        self.label_color.setPixmap(self.color_pixmap)

        self.r = 0
        self.g = 0
        self.b = 0

        self.point_size = 1

        self.x = 250
        self.y = 250

        # BUTTONS
        self.pushButton_color.clicked.connect(self.do_color)
        self.pushButton_exit.clicked.connect(self.exit)
        self.pushButton_save.clicked.connect(self.save)

        self.start()
        self.update_graphic_view.emit()
        # client-----------------

    def start(self):  # ????????????????
        print("start")

        self.my_thread = threading.Thread(target=self.thread_read, args=())
        self.my_thread.start()

        self.get_all_data()

    def exit(self):
        self.client.close()
        self.hide()
        self.parent.parent.show()

        self.parent.parent.reset()

        print("exit")

    def save(self):
        path, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", "", "All Files(*);;")
        saved_pixmap = self.screen_pixmap

        saved_pixmap = saved_pixmap.scaled(350, 350)
        saved_pixmap.save(path if ".jpg" in path else path + ".jpg", "jpg")

    def mouse_update(self, event):
        # print("x = ", event.pos().x(), " y = ", event.pos().y())

        self.x = int(event.scenePos().x() - (event.scenePos().x() % self.point_size))
        self.y = int(event.scenePos().y() - (event.scenePos().y() % self.point_size))

        print("x = ", self.x)
        print("y = ", self.y)

        if not (0 <= self.x <= self.screen_x and 0 <= self.y <= self.screen_y):
            return

        self.draw()

        try:
            self.send_point()
        except Exception as ex:
            print(ex)

    def update(self):
        self.graphicsView.screen_pixmap_box.setPixmap(self.screen_pixmap)

    def thread_read(self):
        try:
            while True:
                # print("reading")
                msg = self.client.do_read()
                print("length: ", len(msg))
                print("msg", msg)
                self.parse(msg)
                # time.sleep(0.2)
        except Exception as ex:
            print(traceback.format_exc())
            print("error with socket: ", ex)
            self.exit()
            pass
        finally:
            print("finally")

    def parse(self, msg: str):
        # print(f"server: {msg}")
        msg = msg.replace('\'', "\"")
        self.msg_json = json.loads(msg)
        print("reading2")

        type = self.msg_json['mode']
        if type == "ALL_DATA":
            self.draw_from_socket_f()
            return
        if type == "SOME_DATA":
            self.draw_from_socket_s()
            return

    def draw(self):
        print("drawing")
        painter = QPainter(self.screen_pixmap)
        pen = QPen()
        pen.setWidth(self.point_size)
        pen.setColor(QColor(self.r, self.g, self.b))
        painter.setPen(pen)
        painter.drawPoint(self.x + int(self.point_size / 2), self.y + int(self.point_size / 2))  # -------
        painter.end()

        self.update_graphic_view.emit()

    def send_point(self):
        img = self.screen_pixmap.toImage()
        r, g, b, a = QColor(img.pixel(self.x, self.y)).getRgb()  # ??????????? + int(self.point_size / 2)

        dict_resp = {}
        dict_resp['mode'] = "SOME_DATA"
        dict_resp['name'] = self.name
        dict_resp['x'] = str(self.x)
        dict_resp['y'] = str(self.y)
        dict_resp['size_x'] = str(self.screen_x)
        dict_resp['size_y'] = str(self.screen_y)

        dict_resp['data'] = str(r).rjust(3, '0') + str(g).rjust(3, '0') + str(b).rjust(3, '0')
        self.client.do_send(str(dict_resp))

    def get_all_data(self):
        dict_resp = {}
        dict_resp['mode'] = "GET_ALL_DATA"
        dict_resp['name'] = self.name

        self.client.do_send(str(dict_resp))

    def draw_from_socket_s(self):  # read part

        if self.msg_json['name'] != self.name:
            return

        painter = QPainter(self.screen_pixmap)
        pen = QPen()
        pen.setWidth(self.point_size)

        x = int(self.msg_json['x'])
        y = int(self.msg_json['y'])

        rgb = self.msg_json['data']

        r = int(rgb[0:3])
        g = int(rgb[3:6])
        b = int(rgb[6:9])

        pen.setColor(QColor(r, g, b))  # (QColor(r, g, b))
        painter.setPen(pen)
        painter.drawPoint(x + int(self.point_size / 2), y + int(self.point_size / 2))

        painter.end()

        self.update_graphic_view.emit()

    def draw_from_socket_f(self):  # read full
        # self.screen_pixmap = QPixmap(self.screen_x, self.screen_y)

        painter = QPainter(self.screen_pixmap)
        pen = QPen()
        pen.setWidth(self.point_size)

        data = self.msg_json['data']

        print("=", len(data), "=")

        x = 0
        y = 0

        # print(f"length: {len(data)} ")
        # print(f"data:={data}=")

        for i in range(0, int(len(data) / 9)):

            b = data[i * 9:i * 9 + 9]
            r = int(b[0:3])
            g = int(b[3:6])
            b = int(b[6:9])

            # print(f"{r} {g} {b}")
            pen.setColor(QColor(r, g, b))  # (QColor(r, g, b))
            painter.setPen(pen)
            painter.drawPoint(x, y)

            if x == (self.screen_x - self.point_size):
                y += self.point_size
                x = 0
                continue
            x += self.point_size

        painter.end()

        self.update_graphic_view.emit()

    def do_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.r, self.g, self.b, a = color.getRgb()
            # print("r: ", self.r)
            # print("g: ", self.g)
            # print("b: ", self.b)

            painter = QPainter(self.color_pixmap)
            pen = QPen()
            pen.setWidth(41)
            pen.setColor(QColor(self.r, self.g, self.b))
            painter.setPen(pen)
            painter.drawPoint(20, 20)
            painter.end()

            self.label_color.setPixmap(self.color_pixmap)
