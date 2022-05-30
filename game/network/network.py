import socket
from threading import Timer, Thread

from PyQt5.QtCore import QThread


# class CustTimer():
#     def __init__(self, time, func):
#         self.time = time
#         self.func = func
#         self.thread = Timer(self.time, self.func)
#
#     def handle_function(self):
#         self.func()
#         self.thread = Timer(self.time, self.func)
#         self.thread.start()
#
#     def start(self):
#         self.thread.start()
#
#     def cancel(self):
#         self.thread.cancel()
#
#
# class MyThread(QThread):
#     def __init__(self, func):
#         Thread.__init__(self)
#         self.func = func
#
#     def run(self):
#         self.func()
#
# class MyTimer(Thread):
#     def __init__(self, event, time, func):
#         Thread.__init__(self)
#         self.stopped = event
#         self.func = func
#         self.time = time
#
#     def run(self):
#         while not self.stopped.wait(self.time):
#             self.func()


class Network:
    def __init__(self):
        self.host = ''
        self.port = 0
        self.msg_size = 0
        self.timeout_read = 0
        self.timeout_conn = 0
        # self.msg = ""
        self.tcpClient = 0

        self.msg_head_size = 0 # const

    def create(self, msg_head_size=5, timeout_read=60, timeout_conn=10):
        self.msg_head_size = msg_head_size
        self.timeout_read = timeout_read
        self.timeout_conn = timeout_conn

    def set_address(self, host, port):
        self.host = host
        self.port = port

    def start(self):
        self.tcpClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.tcpClient.settimeout(self.timeout_conn)
            self.tcpClient.connect((self.host, self.port))
            # print("connected1")
        except socket.timeout:
            print("connection error1 timeout")
            return False
        except Exception:
            print("connection error2 timeout")
            return False
        return True


    def do_send(self, message_send: str):
        print(str(len(message_send)).rjust(self.msg_head_size, '0').encode("utf-8"))
        self.send(str(len(message_send.encode('utf-8'))).rjust(self.msg_head_size, '0'))  # ?
        print(str(message_send).encode("utf-8"))
        self.send(str(message_send))
        print("2")

    def do_read(self) -> str:
        msg_size = self.read(self.msg_head_size)
        print(f"---msg_size: {msg_size}")
        msg = self.read(int(msg_size))
        print(f"---msg: {msg}")
        return msg


    def send(self, msg):
        self.tcpClient.send(msg.encode("utf-8"))

    def recv_timeout(self, msg_size) -> bytes:
        self.tcpClient.settimeout(self.timeout_read)
        data = self.tcpClient.recv(msg_size)
        return data

    def read(self, msg_size):
        data = b''
        buf_size = 0
        while buf_size < msg_size:
            buf = self.recv_timeout(msg_size - buf_size)
            if buf == b'':
                raise ConnectionError
            data += buf
            buf_size += len(buf)
        return data.decode('utf-8')

    def close(self):
        self.tcpClient.close()
