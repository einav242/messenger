import socket
import threading
import tkinter
from tkinter import *
import os
import time
import hashlib
import pickle

HOST = '127.0.0.1'
PORT = 9090


class server:
    def __init__(self):
        self.count = 2
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((HOST, PORT))
        self.soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.soc.bind((HOST, 1234))
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
                if message.decode() == "show_file1234":
                    files = os.listdir()
                    for f in files:
                        if f == "server.py":
                            continue
                        m = str(f) + "\n"
                        client.send(m.encode())
                elif message.decode().split()[0] == "private":
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
                msg, address = self.soc.recvfrom(4096)
                base = 1
                nextSeqnum = 1
                windowSize = 7
                window = []
                file = msg.decode().split()[1]
                name = msg.decode().split()[0]
                for n in self.nicknames:
                    i = str(n.split(":")[0])
                    if i == name:
                        index = self.nicknames.index(n)
                        person = self.clients[index]
                        break
                files = os.listdir()
                if file in files:
                    file_size = os.path.getsize(file)
                    m = "exist" + " " + str(file_size)
                    self.soc.sendto(m.encode(), address)
                    if file_size < 64000:
                        f = open(file, 'rb')
                        data = f.read(500)
                        done = False
                        lastackreceived = time.time()
                        while not done or window:
                            if (nextSeqnum < base + windowSize) and not done:
                                sndpkt = []
                                sndpkt.append(nextSeqnum)
                                sndpkt.append(data)
                                h = hashlib.md5()
                                h.update(pickle.dumps(sndpkt))
                                sndpkt.append(h.digest())
                                self.soc.sendto(pickle.dumps(sndpkt), address)
                                print("Sent data", nextSeqnum)
                                nextSeqnum = nextSeqnum + 1
                                if not data:
                                    done = True
                                window.append(sndpkt)
                                data = f.read(500)
                            try:
                                packet, serverAddress = self.soc.recvfrom(4096)
                                rcvpkt = []
                                rcvpkt = pickle.loads(packet)
                                c = rcvpkt[-1]
                                del rcvpkt[-1]
                                h = hashlib.md5()
                                h.update(pickle.dumps(rcvpkt))
                                if c == h.digest():
                                    print("Received ack for", rcvpkt[0])
                                    while rcvpkt[0] > base and window:
                                        lastackreceived = time.time()
                                        temp = window[0]
                                        del window[0]
                                        base = base + 1
                                else:
                                    print("error detected")
                            except:
                                if time.time() - lastackreceived > 0.01:
                                    for i in window:
                                        self.soc.sendto(pickle.dumps(i), address)
                    f.close()
                    print("connection closed")
                    b = "finish download the last byte is: " + str(temp[-1]) + "\n"
                    person.send(b.encode())
                else:
                    m1 = "not"
                    self.soc.sendto(m1.encode(), address)
                    m = "the file does not exist\n"
                    person.send(m.encode())
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
        self.soc.close()
        self.server.close()
        exit(0)

    def stop(self):
        self.running = False
        self.window.destroy()
        self.soc.close()
        self.server.close()
        exit(0)


server()
