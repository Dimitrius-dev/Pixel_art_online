
class Session:
    def __init__(self):
        self.size_x = 0
        self.size_y = 0
        self.name = "new session"
        self.password = ""
        self.pixmap = ""

    def set_size(self, x, y):
        self.size_x = x
        self.size_y = y

    def get_x(self):
        return self.size_x

    def get_y(self):
        return self.size_y

    def set_session(self, name, password):
        self.name = name
        self.password = password

    def get_name(self):
        return self.name

    def get_password(self):
        return self.password

    def fill_pixmap(self):
        self.pixmap = "255"*3*self.size_x*self.size_y

    def insert_into_pixmap(self, pos, data):
        self.pixmap = self.pixmap[:pos] + str(data) + self.pixmap[pos + len(data):]

    def get_pixmap(self):
        return self.pixmap
