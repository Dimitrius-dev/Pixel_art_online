import sys

from PyQt5 import QtWidgets

from screen.screen1 import Authoriz

if __name__ == "__main__":
    try:
        app = QtWidgets.QApplication(sys.argv)
        ex = Authoriz()
        ex.show()
        sys.exit(app.exec_())
    except:
        pass