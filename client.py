import socket
import threading


class client:
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect(("192.168.1.101", 4434))
        t = threading.Thread(target=self.job)
        t.start()

        while True:
            try:
                print(self.s.recv(1024).decode())

            except:
                pass

    def job(self):
        while True:
            self.s.send(input().encode())


client()
