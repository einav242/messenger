import hashlib
import pickle
import socket
import threading
from tkinter import *
import tkinter.scrolledtext
from tkinter import simpledialog, ttk
import time


class client:
    def __init__(self, host, port):
        self.port = None
        self.bool = False
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((host, port))
        self.temp = tkinter.Tk()
        self.temp.withdraw()
        self.nickname = simpledialog.askstring("Nickname", "please choose a nickname", parent=self.temp)
        self.gui_done = False
        self.running = True
        gui_thread = threading.Thread(target=self.gui_loop)
        receive_thread = threading.Thread(target=self.receive)
        try:
            gui_thread.start()
        except:
            pass
        try:
            receive_thread.start()
        except:
            pass

    def gui_loop(self):
        self.win = Tk()
        self.win.title("client")
        self.win.configure(background="#6F8EB1")

        Button(self.win, text="start", width=12, command=self.write, fg="black", bg="green").grid(row=0, column=0,
                                                                                                  sticky=W)
        Label(self.win, text="name:" + self.nickname + "  address:" + str(self.s.getsockname()), bg="#6F8EB1",
              fg="black", font="Helvetica 11 bold").grid(row=1, column=0, sticky=W)

        Button(self.win, text="Show Online", width=12, command=self.user_list).grid(row=0, column=2, sticky=W)
        Button(self.win, text="Show Server Files", width=12, command=self.show_file).grid(row=2, column=2, sticky=W)

        Label(self.win, text="Chat:", bg="#6F8EB1", fg="black", font="Consolas").grid(row=3, column=0, sticky=W)
        self.input_area = Text(self.win, width=75, height=15, wrap=WORD, background="lightgray")
        self.input_area.grid(row=5, column=0, columnspan=2, sticky=W)

        Label(self.win, text="Message:", bg="#6F8EB1", fg="black", font="Consolas").grid(row=6, column=0, sticky=W)
        self.msg = Entry(self.win, width=40, bg="white")
        self.msg.grid(row=7, column=0, sticky=W)

        Button(self.win, text="Send all", width=12, command=self.write).grid(row=7, column=1, sticky=W)
        Label(self.win, text="To:", bg="#6F8EB1", fg="black", font="Consolas").grid(row=8, column=0, sticky=W)
        self.user = Entry(self.win, width=40, bg="white")
        self.user.grid(row=9, column=0, sticky=W)
        Button(self.win, text="Send private", width=12, command=self.write_to).grid(row=9, column=1, sticky=W)

        Label(self.win, text="Server File Name:", bg="#6F8EB1", fg="black", font="Consolas").grid(row=10, column=0,
                                                                                                  sticky=W)
        self.file = Entry(self.win, width=40, bg="white")
        self.file.grid(row=11, column=0, sticky=W)
        Label(self.win, text="Save as:", bg="#6F8EB1", fg="black", font="Consolas").grid(row=10, column=1, sticky=W)
        self.file_save = Entry(self.win, width=40, bg="white")
        self.file_save.grid(row=11, column=1, sticky=W)
        Button(self.win, text="Download", width=12, command=self.ask_download).grid(row=11, column=2, sticky=W)

        Button(self.win, text=" New Download", width=12, command=self.clear).grid(row=12, column=2, sticky=W)

        Button(self.win, text="Log Out", width=12, command=self.stop, fg="black", bg="red").grid(row=13, column=0,
                                                                                                 sticky=W)

        self.my_progress = ttk.Progressbar(self.win, orient=HORIZONTAL, length=300, mode='determinate')
        self.my_progress.grid(row=12, column=0, sticky=W)

        self.my_label = Label(self.win, text="0%", bg="#6F8EB1", fg="black", font="Consolas")
        self.my_label.grid(row=12, column=0, sticky=W)

        self.gui_done = True

        self.win.protocol("WM_DELETE_WINDOW", self.stop)

        self.win.mainloop()

    def clear(self):
        self.my_progress.stop()
        self.my_label.config(text="0%")

    def show_file(self):
        try:
            message = "show_file1234"
            self.s.send(message.encode())
        except:
            pass

    def ask_download(self):
        if self.file_save.get() != "" and self.file.get() != "":
            m = "DOWNLOAD_ASK" + " " + self.file.get() + " " + self.nickname
            self.s.send(m.encode())

    def download(self):
        try:
            temp2 = None
            temp = 0
            self.soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.soc.settimeout(3)
            message = self.nickname + " " + self.file.get()
            file_save = self.file_save.get()
            expectedseqnum = 1
            f = open(file_save, "wb")
            endoffile = False
            lastpktreceived = time.time()
            starttime = time.time()
            if file_save != "" and self.file.get() != "":
                self.soc.sendto(message.encode(), ("127.0.0.1", self.port))
                size, address = self.soc.recvfrom(4096)
                if size.decode().split()[0] == "exist":
                    total_size = int(size.decode().split()[1])
                    while not endoffile:
                        try:
                            self.rcvpkt = []
                            packet, clientAddress = self.soc.recvfrom(4096)
                            self.rcvpkt = pickle.loads(packet)
                            c = self.rcvpkt[-1]
                            del self.rcvpkt[-1]
                            h = hashlib.md5()
                            h.update(pickle.dumps(self.rcvpkt))
                            if c == h.digest():
                                temp += (len(self.rcvpkt[1]))
                                rate = int((temp / total_size) * 100)
                                self.my_progress['value'] = rate
                                self.my_label.config(text=str(rate) + "%")
                                time.sleep(0.001)
                                self.win.update()
                                if self.rcvpkt[0] == expectedseqnum:
                                    print("Received inorder", expectedseqnum)
                                    if self.rcvpkt[1]:
                                        f.write(self.rcvpkt[1])
                                        try:
                                            temp2 = self.rcvpkt[1][-1]
                                        except:
                                            pass
                                    else:
                                        endoffile = True
                                    expectedseqnum = expectedseqnum + 1
                                    sndpkt = []
                                    sndpkt.append(expectedseqnum)
                                    h = hashlib.md5()
                                    h.update(pickle.dumps(sndpkt))
                                    sndpkt.append(h.digest())
                                    self.soc.sendto(pickle.dumps(sndpkt), (clientAddress[0], clientAddress[1]))
                                    print("New Ack", expectedseqnum)
                                else:
                                    print("Received out of order", self.rcvpkt[0])
                                    sndpkt = []
                                    sndpkt.append(expectedseqnum)
                                    h = hashlib.md5()
                                    h.update(pickle.dumps(sndpkt))
                                    sndpkt.append(h.digest())
                                    self.soc.sendto(pickle.dumps(sndpkt), (clientAddress[0], clientAddress[1]))
                                    print("Ack", expectedseqnum)
                            else:
                                print("error detected")
                        except:
                            if endoffile:
                                if time.time() - lastpktreceived > 3:
                                    break

                    endtime = time.time()

                    f.close()
                    print('FILE TRANFER SUCCESSFUL')
                    print("TIME TAKEN ", str(endtime - starttime))
                    m = "finish download " + self.file.get() + " the last byte is: " + str(temp2) + "\n"
                    self.input_area.config(state='normal')
                    self.input_area.insert(END, m)
                    self.input_area.yview('end')
                    self.input_area.config(state='disabled')


        except:
            pass
        self.file.delete(0, END)
        self.file_save.delete(0, END)
        self.soc.close()

    def user_list(self):
        message = "send1234"
        self.s.send(message.encode())

    def write_to(self):
        name = self.user.get()
        message = f"private message to {name}\n {self.nickname}: {self.msg.get()}" + "\n"
        try:
            self.s.send(message.encode())
            self.msg.delete(0, END)
            self.user.delete(0, END)
        except:
            pass

    def write(self):
        message = f"{self.nickname}: {self.msg.get()}" + "\n"
        self.s.send(message.encode())
        self.msg.delete(0, END)

    def stop2(self):
        self.running = False
        self.msg.destroy()
        self.s.close()
        self.soc.close()
        exit(0)

    def stop(self):
        self.running = False
        self.win.destroy()
        self.s.close()
        try:
            self.soc.close()
        except:
            pass

        exit(0)

    def receive(self):
        while self.running:
            try:
                message = self.s.recv(1024)
                try:
                    if self.bool == False:
                        self.port = int(message.split()[1])
                        print(self.port)
                        self.bool = True
                except:
                    pass
                if message.split()[0] == "NICK":
                    self.port = message.split()[1]
                    self.s.send(self.nickname.encode())
                elif message.decode() == "start download the file...":
                    self.download()
                else:
                    if self.gui_done:
                        self.input_area.config(state='normal')
                        self.input_area.insert(END, message)
                        self.input_area.yview('end')
                        self.input_area.config(state='disabled')

                        # self.text_area.config(state='normal')
                        # self.text_area.insert('end', message)
                        # self.text_area.yview('end')
                        # self.text_area.config(state='disabled')
            except ConnectionAbortedError:
                break
            except:
                self.s.close()
                print("Error")
                exit(0)


client("127.0.0.1", 9090)
