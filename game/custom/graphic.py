from PyQt5.QtCore import QEvent, pyqtSignal
from PyQt5.QtGui import QBrush, QColor
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsPixmapItem
from PyQt5 import QtWidgets, QtCore


class MyScene(QGraphicsScene):
    clicked = pyqtSignal(QEvent)

    def __init__(self):
        super(MyScene, self).__init__()

    def mousePressEvent(self, event):
        super(MyScene, self).mousePressEvent(event)
        # print('mouse pressed inside view')
        print(event.scenePos().x(), " - ", event.scenePos().y())

        self.clicked.emit(event)


class MyGraphicView(QtWidgets.QGraphicsView):

    def __init__(self, parent):
        super(MyGraphicView, self).__init__(parent)
        self.screen_pixmap_box = QGraphicsPixmapItem()
        self.scene = MyScene()  # QGraphicsScene()

        # self.screen_pixmap_box.pixmap().fill(QColor(150, 150, 150))
        background_brush = QBrush(QColor(209, 219, 228), QtCore.Qt.SolidPattern)
        self.setBackgroundBrush(background_brush)

        self.scene.addItem(self.screen_pixmap_box)
        self.setScene(self.scene)

        self.zoom = 0

        self.x = 0
        self.y = 0

    def wheelEvent(self, event):
        if event.angleDelta().y() > 0:
            print("+")
            self.zoom += 1
            factor = 1.25
        else:
            print("-")
            self.zoom -= 1
            factor = 0.8

        self.scale(factor, factor)