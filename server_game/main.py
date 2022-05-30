import socket

# import thread module
from _thread import *
import threading
from parser import *

from config import host_server, port_server


# utf-8 is not supported


class ClientThread(threading.Thread):
    msg: str

    def __init__(self, ip, port, socket, clients, sessions):
        threading.Thread.__init__(self)

        self.timeout_read = 120  # seconds

        self.ip = ip
        self.port = port
        self.socket = socket

        self.msg_head_size = 6

        self.clients = clients
        self.sessions = sessions

        self.parser = Parser(self.sessions)
        print("[+] New thread started for " + ip + ":" + str(port))

    # def update_pixmap_f(self):
    #     mutex.acquire()
    #     try:
    #         self.pixmap[0] = self.msg
    #     finally:
    #         mutex.release()
    #
    # def replace_pixmap(self, pos, data):
    #     self.pixmap[0] = (self.pixmap[0])[:pos] + str(data) + (self.pixmap[0])[pos + len(data):]

    # def update_pixmap_p(self):
    #     mutex.acquire()
    #     try:
    #         b = self.msg
    #         x = int(b[0:4])
    #         y = int(b[4:8])
    #
    #         color = str(b[8:17])
    #
    #         self.replace_pixmap(y * 25 * 9 + x * 9, color)
    #         print("msg len up:", len(self.pixmap[0]))
    #     finally:
    #         mutex.release()

    def recv_timeout(self, msg_size) -> bytes:
        self.socket.settimeout(self.timeout_read)
        data = self.socket.recv(msg_size)
        return data

    def read(self, msg_size):
        print("msg_size", msg_size)

        data = b''
        buf_size = 0
        while buf_size < msg_size:
            buf = self.recv_timeout(msg_size - buf_size)

            print("buf", buf)

            if buf == b'':
                raise ConnectionError
            data += buf
            buf_size += len(buf)

            print("buf_size", buf_size)

        return data.decode('utf-8')

    def do_read(self) -> str:
        msg_size = self.read(self.msg_head_size)
        print("size:", msg_size)
        msg = self.read(int(msg_size))
        print("msg:", msg)
        return msg

    def do_send(self, msg, client):
        a = (str(len(msg)).rjust(self.msg_head_size, '0'))
        b = msg.encode('utf-8')
        print("a:", a)
        print("b:", b)
        client.send(str(len(msg.encode('utf-8'))).rjust(self.msg_head_size, '0').encode('utf-8'))
        client.send(msg.encode('utf-8'))

    def run(self):
        try:
            while True:
                msg = self.do_read()
                # print("msg: ", msg)

                response = self.parser.get_response(msg)

                if not response:
                    continue

                if self.parser.is_all():
                    for c in self.clients:
                        self.do_send(response, c)
                else:
                    for c in self.clients:
                        if int(c.fileno()) == int(self.socket.fileno()):
                            self.do_send(response, c)
                            break

        except Exception as ex:
            print(ex)
            self.socket.close()
            self.clients.remove(self.socket)
            print("connection closed")


if __name__ == '__main__':

    sessions = []
    client_list = []

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host_server, port_server))
    print("socket binded to port", port_server, "\nip: ", host_server)

    s.listen(5)

    while True:
        (clientsock, (ip, port)) = s.accept()
        client_list.append(clientsock)
        new_thread = ClientThread(ip, port, clientsock, client_list, sessions)
        new_thread.start()
