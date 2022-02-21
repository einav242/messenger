import socket
import select
import threading
import tkinter
from tkinter import *

HOST = '127.0.0.1'
PORT = 9090


class server2:
    def __init__(self):
        self.count = 2
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((HOST, PORT))
        self.server.listen(5)
        self.clients = []
        self.nicknames = []
        self.running = True
        try:
            gui_thread = threading.Thread(target=self.gui_loop)
            gui_thread.start()
        except:
            pass
        self.receive()

    def broadcast(self, message, non_receptors=None):
        if non_receptors is None:
            for client in self.clients:
                client.send(message)
        else:
            for client in self.clients:
                if client == non_receptors:
                    continue
                client.send(message)

    def receive(self):
        while self.running:
            # try:
                client, address = self.server.accept()
                print(f"Connected with {str(address)}!")

                client.send("NICK".encode('utf-8'))
                nickname = client.recv(1024)

                name = nickname.decode()

                self.nicknames.append(name)

                self.clients.append(client)

                Label(self.window, text="connected to new client " + str(name), bg="white", fg="black",
                      font="none 12 bold").grid(row=self.count, column=0, sticky=W)
                self.count += 1
                self.broadcast(f"{name} connected to the server! \n".encode())
                names = []
                for n in self.nicknames:
                    if n is not client:
                        print(n)
                        names.append(n)
                print(names)
                m = "hello user! \n users online: " + str(names) + "\n"
                m2 = "users online: " + str(names) + "\n"
                self.broadcast(m2.encode(), client)
                client.send(m.encode())
                # client.send("Connected to the server".encode())

                thread = threading.Thread(target=self.handle, args=(client,))
                thread.start()
            # except:
            #     break

    def handle(self, client):
        while True:
            try:
                message = client.recv(1024)
                print(f"{self.nicknames[self.clients.index(client)]} says {message}")
                self.broadcast(message)
            except:
                index = self.clients.index(client)
                self.clients.remove(client)
                client.close()
                nickname = self.nicknames[index]
                self.nicknames.remove(nickname)
                names = [n for n in self.nicknames if n is not client and n is not self.server]
                name = nickname.split()[0]
                m = f"{name} leave\n users online: " + str(names)
                self.broadcast(m.encode())
                Label(self.window, text=str(name)+"left", bg="white", fg="black",
                      font="none 12 bold").grid(row=self.count, column=0, sticky=W)
                self.count += 1
                break

    def gui_loop(self):
        self.window = Tk()
        self.window.title("server")
        self.window.configure(background="white")
        Label(self.window, text="starting sever...", bg="white", fg="black",
              font="none 12 bold").grid(row=1, column=0, sticky=W)
        Label(self.window, text="                                                      ", bg="white", fg="black",
              font="none 12 bold").grid(row=1, column=1, sticky=W)

        self.window.protocol("WM_DELETE_WINDOW", self.stop)

        self.window.mainloop()

    def stop(self):
        self.running = False
        self.window.destroy()
        self.server.close()
        exit(0)


print("server runnig....")
server2()
