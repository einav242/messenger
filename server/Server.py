import socket
import threading
import tkinter
from tkinter import *
import os
import time
import hashlib
import pickle

HOST = '127.0.0.1'
PORT = 50500


class server:
    def __init__(self):
        self.port = 50000
        self.count = 2
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # open tcp socket
        self.server.bind((HOST, PORT))
        self.server.listen(15)  # listen to 15 clients in the same time
        self.clients = []  # list of clients
        self.nicknames = []  # list of the nickname of the client
        self.udp_port = dict()  # each client has a udp port so the server can send a file in paralle
        self.stop_download = dict()  # if the client want to stop the download in the key of his name we chance to true
        self.wait = dict()  # after the server download 50% of the file we chance the value that in key of the name of
        # the client to be true and if the client want to continue the download in we chance it to true
        self.running = True  # for the gui and for the server to know when to stop to listen
        try:
            gui_thread = threading.Thread(target=self.gui_loop)
            gui_thread.start()
        except:
            pass
        try:
            self.receive()
        except:
            pass

    # function that send a message to everyone except "non_receptors"
    def send_message(self, message, non_receptors=None):
        try:
            if non_receptors is None:
                for client in self.clients:
                    client.send(message)
            else:
                for client in self.clients:
                    if client == non_receptors:
                        continue
                    client.send(message)
        except:
            pass

    def receive(self):
        while self.running:
            try:
                client, address = self.server.accept()  # when a client connected to the server

                m = "NICK" + " " + str(self.port)
                # ask for the nickname of the client and send a port number for the udp connection
                client.send(m.encode('utf-8'))
                nickname = client.recv(1024)

                name = nickname.decode().split(":")[0]

                self.udp_port[name] = self.port
                self.port += 1  # for the next client the connected

                self.nicknames.append(name)

                self.stop_download[name] = False

                self.wait[name] = False

                self.clients.append(client)

                Label(self.window, text="connected with " + str(address) + " nickname: " + str(name), bg="white",
                      fg="black",
                      font="none 12 bold").grid(row=self.count, column=0, sticky=W)
                self.count += 1

                self.send_message(f"{name} connected to the server! \n".encode())
                # send to everyone that "name" connect to the server
                names = [n for n in self.nicknames if n is not client and n is not self.server]
                #  send to the client all the clients that connect
                m = "hello user! \n users online: " + str(names) + "\n"
                m2 = "users online: " + str(names) + "\n"
                self.send_message(m2.encode(), client)
                client.send(m.encode())
                try:
                    thread = threading.Thread(target=self.get_message, args=(client, name,))
                    # each client has their own thread
                    thread.start()
                except:
                    break
            except:
                break

    def get_message(self, client, nick):  # over of all the types of messages and sends a response message respectively
        self.temp = -1
        while True:
            try:
                message = client.recv(1024)  # get a message from the client on tcp connection
            except:
                pass
            try:
                if message.decode() == "show_file1234":  # the client want to see the file that inside the server folder
                    files = os.listdir()
                    for f in files:
                        if f == "Server.py":
                            continue
                        m = str(f) + "\n"
                        client.send(m.encode())
                elif message.decode() == "END_CONNECTION":  # the client want to disconnect
                    index = self.clients.index(client)
                    self.clients.remove(client)
                    client.close()
                    nickname = self.nicknames[index]
                    del self.udp_port[nickname]
                    self.nicknames.remove(nickname)
                    name = nickname.split()[0]
                    m = f"{name} leave\n"
                    self.send_message(m.encode())
                    Label(self.window, text=str(name) + " left", bg="white", fg="black",
                          font="none 12 bold").grid(row=self.count, column=0, sticky=W)
                    self.count += 1
                    break
                elif message.decode().split()[0] == "DOWNLOAD_ASK":  # ask for download a file
                    file_name = message.decode().split()[1]
                    name = message.decode().split()[2]
                    files = os.listdir()
                    if file_name in files:  # checking if the file inside of the folder server
                        m = "start download the file..."
                        client.send(m.encode())
                        self.stop_download[nick] = False
                        self.wait[nick] = False
                        self.file_thread = threading.Thread(target=self.download_file, args=(file_name, name,))
                        self.file_thread.start()
                    else:
                        m = "the file " + file_name + " does not exist\n"
                        client.send(m.encode())
                elif message.decode() == "YES CONTINUE":  # continue to download the file
                    self.wait[nick] = False
                elif message.decode() == "STOP DOWNLOAD!":  # stop the download the file
                    self.port += 1  # chence udp port for the client
                    new_port = "NEWPORT" + " " + str(self.port)
                    client.send(new_port.encode())
                    # sending to the client a new port because the socket may be still on when we try to download again
                    self.udp_port[nick] = self.port
                    self.stop_download[nick] = True  # that make to stop download the file
                elif message.decode().split()[0] == "private":  # the client want to sent a private message
                    user = message.decode().split()[3]  # the name of who the client want to send a message
                    for n in self.nicknames:  # to find the right client to send the message
                        i = str(n.split(":")[0])
                        if i == user:
                            index = self.nicknames.index(n)
                            person = self.clients[index]
                            person.send(message)
                            client.send(message)
                            self.temp = 0
                            break
                    if self.temp != 0:  # if the client does not exist
                        msg = f"user {user} not found \n"
                        client.send(msg.encode())
                    self.temp = -1
                elif message.decode() == "send1234":  # the client want to know the name of the client that connected
                    names = [n for n in self.nicknames if n is not client and n is not self.server]
                    m = "users online: " + str(names) + "\n"
                    client.send(m.encode())
                else:  # send everyone that connected the message
                    self.send_message(message)
            except:
                pass

    def download_file(self, file_name, name):
        x = 1
        try:
            x = 1
            first = 1
            nextS = 1
            windowSize = 7
            window = []
            once = False
            index = self.nicknames.index(name)
            person = self.clients[index]
            temp = 0
            port = self.udp_port[name]
            soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # open udp socket
            soc.settimeout(3)
            soc.bind((HOST, port))
            msg, c_address = soc.recvfrom(5120)
            file_size = os.path.getsize(file_name)
            m = "exist" + " " + str(file_size)
            soc.sendto(m.encode(), c_address)
            if file_size <= 65536:
                f = open(file_name, 'rb')  # open the file to send to the client
                data = f.read(x)
                finish = False
                start_time = time.time()
                while not finish or window:
                    if self.stop_download[name]:
                        soc.close()
                        break
                    if self.wait[name]:
                        time.sleep(1)
                        continue
                    if (nextS < first + windowSize) and not finish:  # to check is the next date is in the window
                        sndpkt = []
                        sndpkt.append(nextS)
                        sndpkt.append(data)
                        h = hashlib.md5()
                        h.update(pickle.dumps(sndpkt))
                        sndpkt.append(h.digest())
                        temp += len(data)
                        rate = int((temp / file_size) * 100)
                        if rate == 50 and once == False:
                            # if we send 50% of the file to the client we wait for client to dicide if continue or not
                            self.wait[name] = True
                            stop_msg = "STOP AND WAIT"
                            person.send(stop_msg.encode())
                            once = True
                        soc.sendto(pickle.dumps(sndpkt), c_address)  # send to the client the packet
                        nextS = nextS + 1
                        if not data:
                            finish = True
                        window.append(sndpkt)
                        data = f.read(x)
                        try:
                            packet, client_address = soc.recvfrom(5120)
                            rcvpkt = []
                            rcvpkt = pickle.loads(packet)
                            c = rcvpkt[-1]
                            del rcvpkt[-1]
                            h = hashlib.md5()
                            h.update(pickle.dumps(rcvpkt))
                            if c == h.digest():
                                if rcvpkt[0] > first and window:
                                    start_time = time.time()
                                    del window[0]
                                    first = first + 1
                            else:
                                print("error detected")
                        except:
                            x = 1024
                            if time.time() - start_time > 0.01:
                                for i in window:
                                    soc.sendto(pickle.dumps(i), c_address)
                f.close()
                soc.close()
                self.stop_download[name] = False
        except:
            x = 1024
            pass

    def gui_loop(self):
        try:
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
        except:
            pass

    def log_out(self):
        try:
            self.running = False
            self.window.destroy()
            self.server.close()
            os._exit(0)
        except:
            pass

    def stop(self):
        try:
            self.running = False
            self.window.destroy()
            self.server.close()
            os._exit(0)
        except:
            pass


server()
