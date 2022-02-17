import socket
import select
import threading
from tkinter import *


class server:
    def __init__(self):
        self.count = 2
        self.window = None
        self.server = socket.socket()
        self.inputs = [self.server]
        self.server.bind(("192.168.1.101", 4434))
        self.server.listen(5)
        self.t = threading.Thread(target=self.send)
        self.t.start()
        self.draw()

    def notify_all(self, msg, non_receptors):
        for connection in self.inputs:
            if connection not in non_receptors:
                connection.send(msg)

    def greet(self, client):
        names = [n.getpeername() for n in self.inputs if n is not client and n is not self.server]
        m = "hello user! \n users online: " + str(names)
        client.send(m.encode())

    def draw(self):
        self.window = Tk()
        self.window.title("server")
        self.window.configure(background="white")
        Label(self.window, text="starting sever...", bg="white", fg="black",
              font="none 12 bold").grid(row=1, column=0, sticky=W)
        Label(self.window, text="                                                      ", bg="white", fg="black",
              font="none 12 bold").grid(row=1, column=1, sticky=W)
        self.window.mainloop()
        for n in self.inputs:
            n.close()

    def send(self):
        while self.inputs:
            try:
                readables, _, _ = select.select(self.inputs, [], [])
            except:
                break
            for i in readables:
                if i is self.server:
                    try:
                        client, address = self.server.accept()
                    except:
                        break
                    self.inputs.append(client)
                    Label(self.window, text="connected to new client", bg="white", fg="black",
                          font="none 12 bold").grid(row=self.count, column=0, sticky=W)
                    self.count += 1
                    self.greet(client)
                    self.notify_all(f"client {address} enterd".encode(), [self.server, client])
                else:
                    try:
                        data = i.recv(1024)
                        msg = str(str(i.getpeername()) + ">>> " + data.decode()).encode()
                        self.notify_all(msg, [self.server, i])
                    except:
                        self.inputs.remove(i)
                        Label(self.window, text=f"client {i.getpeername()} leave", bg="white", fg="black",
                              font="none 12 bold").grid(row=self.count, column=0, sticky=W)
                        self.count += 1
                        self.notify_all(f"client {i.getpeername()} left".encode(), [self.server])
                        i.close()


server()
