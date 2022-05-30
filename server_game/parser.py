import threading

from session import *
from enum import Enum
import json


# class State(Enum):
#     DEFAULT = 0
#     GET_ALL_DATA = 1
#     GET_DATA = 2
#     ADD_SESSION = 3


class Parser:
    def __init__(self, sessions):

        self.mutex = threading.Lock()

        self.input_msg = ""
        self.data = None
        self.answer_msg = ""
        self.state = 0

        self.multi = False

        self.sessions = sessions

    def get_response(self, input_msg):
        # self.mutex.acquire() # _____

        self.input_msg = input_msg

        data = input_msg.replace('\'', "\"")
        data = json.loads(data)
        self.data = data

        type = data['mode']

        if type == "CREATE":
            self.multi = False
            return self.create_session()
        if type == "DELETE":
            self.multi = False
            return self.delete_session()
        if type == "GET_SERVERS":
            self.multi = False
            return self.servers()
        if type == "GET_SERVER":
            self.multi = False
            return self.server()

        if type == "GET_ALL_DATA":
            self.multi = False
            return self.all_data()
        if type == "SOME_DATA":
            self.multi = True
            return self.some_data()

        # self.mutex.release() # _____

    def is_all(self) -> bool:
        return self.multi

    def create_session(self):
        ses = Session()
        ses.set_session(self.data['name'], self.data['password'])

        ses.set_size(int(self.data['x']), int(self.data['y']))
        ses.fill_pixmap()
        self.sessions.append(ses)

        for i in self.sessions:
            print("obj: ", i.get_name())

        return ""

    def delete_session(self):
        for i in self.sessions:
            if i.get_name() == self.data['name']:
                self.sessions.remove(i)
                break

        return ""

    def servers(self):
        dict_resp = {}
        dict_resp['mode'] = "SERVERS"
        servers = {}
        for s in self.sessions:
            servers[str(self.sessions.index(s))] = s.get_name()
        dict_resp['list'] = servers

        print("dawwfawfawawf")
        print(dict_resp)

        return str(dict_resp)

    def server(self):
        dict_resp = {}
        for s in self.sessions:
            print("naaaame: ", s.get_name())
            if s.get_name() == self.data['name']:
                dict_resp['mode'] = "SERVER"
                dict_resp['x'] = s.get_x()
                dict_resp['y'] = s.get_y()
                dict_resp['password'] = s.get_password()
                return str(dict_resp)

        dict_resp['mode'] = "ERROR"
        return str(dict_resp)

    def all_data(self):
        for s in self.sessions:
            if s.get_name() == self.data['name']:
                dict_resp = {}
                dict_resp['mode'] = "ALL_DATA"
                dict_resp['name'] = self.data['name']
                dict_resp['data'] = s.get_pixmap()
                return str(dict_resp)
        return ""

    def some_data(self):
        x = int(self.data['x'])
        y = int(self.data['y'])
        size_x = int(self.data['size_x'])
        size_y = int(self.data['size_y'])
        pos = y * 9 * size_y + x * 9

        for s in self.sessions:
            if s.get_name() == self.data['name']:
                s.insert_into_pixmap(pos, self.data['data'])
                break

        print("some data:", self.data)

        return str(self.data)
