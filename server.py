import socket
import select
import threading
import tkinter
from tkinter import *
import os

HOST = '127.0.0.1'
PORT = 9090


class server:
    def __init__(self):
        self.count = 2
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((HOST, PORT))
        self.soc = socket.socket()
        self.soc.bind((HOST, 1234))
        self.soc.listen(15)
        self.server.listen(15)
        self.clients = []
        self.nicknames = []
        self.running = True
        try:
            gui_thread = threading.Thread(target=self.gui_loop)
            gui_thread.start()
        except:
            pass
        try:
            file_thread = threading.Thread(target=self.send_file)
            file_thread.start()
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
            try:
                client, address = self.server.accept()

                client.send("NICK".encode('utf-8'))
                nickname = client.recv(1024)

                name = nickname.decode().split(":")[0]

                self.nicknames.append(name)

                self.clients.append(client)

                Label(self.window, text="connected with " + str(address) + " nickname: " + str(name), bg="white",
                      fg="black",
                      font="none 12 bold").grid(row=self.count, column=0, sticky=W)
                self.count += 1
                self.broadcast(f"{name} connected to the server! \n".encode())
                names = [n for n in self.nicknames if n is not client and n is not self.server]
                m = "hello user! \n users online: " + str(names) + "\n"
                m2 = "users online: " + str(names) + "\n"
                self.broadcast(m2.encode(), client)
                client.send(m.encode())
                try:
                    thread = threading.Thread(target=self.handle, args=(client,))
                    thread.start()
                except:
                    break
            except:
                break

    def handle(self, client):
        self.temp = -1
        while True:
            try:
                message = client.recv(1024)
                if message.decode().split()[0] == "private":
                    user = message.decode().split()[1]
                    for n in self.nicknames:
                        i = str(n.split(":")[0])
                        if i == user:
                            index = self.nicknames.index(n)
                            person = self.clients[index]
                            person.send(message)
                            client.send(message)
                            self.temp = 0
                            break
                    if self.temp != 0:
                        msg = f"user {user} not found \n"
                        client.send(msg.encode())
                    self.temp = -1
                elif message.decode() == "send1234":
                    names = [n for n in self.nicknames if n is not client and n is not self.server]
                    m = "users online: " + str(names) + "\n"
                    client.send(m.encode())
                else:
                    self.broadcast(message)
            except:
                index = self.clients.index(client)
                self.clients.remove(client)
                client.close()
                nickname = self.nicknames[index]
                self.nicknames.remove(nickname)
                name = nickname.split()[0]
                m = f"{name} leave\n"
                self.broadcast(m.encode())
                Label(self.window, text=str(name) + " left", bg="white", fg="black",
                      font="none 12 bold").grid(row=self.count, column=0, sticky=W)
                self.count += 1
                break

    def send_file(self):
        while self.running:
            try:
                client, address = self.soc.accept()
                nickname = client.recv(1024)
                print(nickname.decode())
            except:
                break

    def gui_loop(self):
        self.window = Tk()
        self.window.title("server")
        self.window.configure(background="white")
        Label(self.window, text="starting sever...", bg="white", fg="black",
              font="none 12 bold").grid(row=1, column=0, sticky=W)
        Label(self.window, text="                                                      ", bg="white", fg="black",
              font="none 12 bold").grid(row=1, column=1, sticky=W)
        Button(self.window, text="LogOut", width=14, command=self.log_out).grid(row=1, column=2, sticky=W)

        self.window.protocol("WM_DELETE_WINDOW", self.stop)

        self.window.mainloop()

    def log_out(self):
        self.running = False
        self.window.destroy()
        self.server.close()
        self.soc.close()
        exit(0)

    def stop(self):
        self.running = False
        self.window.destroy()
        self.server.close()
        self.soc.close()
        exit(0)


server()
