import socket
import select
import threading
import tkinter
from tkinter import *

HOST = '127.0.0.1'
PORT = 9090


class server2:
    def __init__(self):
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

    def broadcast(self, message):
        for client in self.clients:
            client.send(message)

    def receive(self):
        while self.running:
            try:
                client, address = self.server.accept()
                print(f"Connected with {str(address)}!")

                client.send("NICK".encode('utf-8'))
                nickname = client.recv(1024)

                name = nickname.split()[0]

                self.nicknames.append(name)
                self.clients.append(client)

                print(f"Nickname of client is {name}")
                self.broadcast(f"{nickname} connected to the server! \n".encode())
                names = [n for n in self.nicknames if n is not client and n is not self.server]
                m = "hello user! \n users online: " + str(names)+"\n"
                client.send(m.encode())
                # client.send("Connected to the server".encode())

                thread = threading.Thread(target=self.handle, args=(client,))
                thread.start()
            except:
                break

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
                name=nickname.split()[0]
                m = f"{name} leave\n users online: " + str(names)
                self.broadcast(m.encode())
                break

    def gui_loop(self):
        self.win = tkinter.Tk()
        self.win.configure(bg="lightgray")

        self.win.protocol("WM_DELETE_WINDOW", self.stop)

        self.win.mainloop()

    def stop(self):
        self.running = False
        self.win.destroy()
        self.server.close()
        exit(0)


print("server runnig....")
server2()
