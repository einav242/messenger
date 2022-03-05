import hashlib
import pickle
import socket
import threading
from tkinter import *
import os
import tkinter.scrolledtext
from tkinter import simpledialog, ttk
import time


class client:
    def __init__(self, host, port2):
        self.running = True
        self.port = None
        self.bool = False
        self.wait = False
        self.stop_download = False
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # open tcp socket
        self.s.connect((host, port2))  # connected to the server
        self.temp = tkinter.Tk()
        self.temp.withdraw()
        self.nickname = simpledialog.askstring("Nickname", "please choose a nickname", parent=self.temp)
        self.gui_done = False
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
        try:
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

            Button(self.win, text="Log Out", width=12, command=self.stop, fg="black", bg="red").grid(row=17, column=0,
                                                                                                     sticky=W)

            self.my_progress = ttk.Progressbar(self.win, orient=HORIZONTAL, length=300, mode='determinate')
            self.my_progress.grid(row=12, column=0, sticky=W)

            self.my_label = Label(self.win, text="0%", bg="#6F8EB1", fg="black", font="Consolas")
            self.my_label.grid(row=12, column=0, sticky=W)

            self.gui_done = True

            self.win.protocol("WM_DELETE_WINDOW", self.stop)

            self.win.mainloop()
        except:
            pass

    def clear(self):
        try:
            self.my_progress.stop()
            self.my_label.config(text="0%")
        except:
            pass

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
            self.stop_download = False
            self.wait = False
            last_byte = None
            temp = 0
            expectS = 1
            done = False
            self.soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.soc.settimeout(3)
            file_save = self.file_save.get()
            f = open(file_save, "wb")
            last_pkt_received = time.time()
            start_time = time.time()
            message = self.nickname + " " + self.file.get()
            self.soc.sendto(message.encode(), ("127.0.0.1", self.port))
            size, server_address = self.soc.recvfrom(5120)
            if size.decode().split()[0] == "exist":
                total_size = int(size.decode().split()[1])
                while not done:
                    try:
                        if self.stop_download:
                            break
                        if self.wait:
                            continue
                        self.rcvpkt = []
                        packet, server_address = self.soc.recvfrom(5120)
                        self.rcvpkt = pickle.loads(packet)
                        c = self.rcvpkt[-1]
                        del self.rcvpkt[-1]
                        h = hashlib.md5()
                        h.update(pickle.dumps(self.rcvpkt))
                        if c == h.digest():
                            temp += (len(self.rcvpkt[1]))
                            rate = int((temp / total_size) * 100)
                            if rate > 100:
                                rate = 100
                            self.my_progress['value'] = rate
                            self.my_label.config(text=str(rate) + "%")
                            self.win.update()
                            if self.rcvpkt[0] == expectS:
                                if self.rcvpkt[1]:
                                    f.write(self.rcvpkt[1])
                                    last_byte = self.rcvpkt[1][-1]
                                else:
                                    done = True
                                expectS = expectS + 1
                                sndpkt = []
                                sndpkt.append(expectS)
                                h = hashlib.md5()
                                h.update(pickle.dumps(sndpkt))
                                sndpkt.append(h.digest())
                                self.soc.sendto(pickle.dumps(sndpkt), (server_address[0], server_address[1]))
                            else:
                                sndpkt = []
                                sndpkt.append(expectS)
                                h = hashlib.md5()
                                h.update(pickle.dumps(sndpkt))
                                sndpkt.append(h.digest())
                                self.soc.sendto(pickle.dumps(sndpkt), (server_address[0], server_address[1]))
                        else:
                            print("error detected")
                    except:
                        if done:
                            if time.time() - last_pkt_received > 0.1:
                                break

                endtime = time.time()

                if not self.stop_download:
                    f.close()
                    m = "finish download " + self.file.get() + " the last byte is: " + str(last_byte) + "\n" \
                        + "Time taken: " + str(endtime - start_time) + "\n"
                    self.input_area.config(state='normal')
                    self.input_area.insert(END, m)
                    self.input_area.yview('end')
                    self.input_area.config(state='disabled')
                else:
                    f.close()
                    m = "Stop download " + self.file.get() + " the last byte is: " + str(last_byte) + "\n" \
                        + "Time taken: " + str(endtime - start_time) + "\n"
                    self.input_area.config(state='normal')
                    self.input_area.insert(END, m)
                    self.input_area.yview('end')
                    self.input_area.config(state='disabled')
                    self.stop_download = False

                self.file.delete(0, END)
                self.file_save.delete(0, END)
                self.soc.close()
        except:
            pass

    def yes_button(self):
        yes_msg = "YES CONTINUE"
        self.s.send(yes_msg.encode())
        self.wait = False
        self.temp1.destroy()
        self.temp2.destroy()
        self.temp3.destroy()

    def no_button(self):
        no_msg = "STOP DOWNLOAD!"
        self.s.send(no_msg.encode())
        self.temp1.destroy()
        self.temp2.destroy()
        self.temp3.destroy()
        self.stop_download = True

    def user_list(self):
        message = "send1234"
        self.s.send(message.encode())

    def write_to(self):
        name = self.user.get()
        message = f"private message to {name}\n {self.nickname}: {self.msg.get()}" + "\n"
        self.s.send(message.encode())
        self.msg.delete(0, END)
        self.user.delete(0, END)

    def write(self):
        message = f"{self.nickname}: {self.msg.get()}" + "\n"
        self.s.send(message.encode())
        self.msg.delete(0, END)

    def stop(self):
        end_m = "END_CONNECTION"
        self.s.send(end_m.encode())
        self.running = False
        self.win.destroy()
        self.s.close()
        # self.soc.close()
        os._exit(0)

    def receive(self):
        while self.running:
            try:
                message = self.s.recv(1024)
                try:
                    if self.bool == False:
                        self.port = int(message.split()[1])
                        self.bool = True
                except:
                    pass
                try:
                    if message.split()[0] == "NICK":
                        self.port = message.split()[1]
                        self.s.send(self.nickname.encode())
                    elif message.decode() == "start download the file...":
                        try:
                            self.stop_download = False
                            download_thread = threading.Thread(target=self.download)
                            download_thread.start()
                        except:
                            pass
                    elif message.decode() == "STOP AND WAIT":
                        self.wait = True
                        try:
                            self.temp1 = Label(self.win, text="Do you want to continue?", bg="white", fg="black",
                                               font="Helvetica 11 bold")
                            self.temp1.grid(row=13, column=0, sticky=W)
                            self.temp2 = Button(self.win, text="yes", width=12, command=self.yes_button, fg="black",
                                                bg="white")
                            self.temp2.grid(row=14, column=0, sticky=W)
                            self.temp3 = Button(self.win, text="No", width=12, command=self.no_button, fg="black",
                                                bg="white")
                            self.temp3.grid(row=14, column=1, sticky=W)
                        except:
                            pass
                    elif message.decode().split()[0] == "NEWPORT":
                        self.port = int(message.decode().split()[1])
                    else:
                        if self.gui_done:
                            self.input_area.config(state='normal')
                            self.input_area.insert(END, message)
                            self.input_area.yview('end')
                            self.input_area.config(state='disabled')
                except:
                    continue
            except ConnectionAbortedError:
                break
            except:
                self.s.close()
                print("Error")
                exit(0)


client("127.0.0.1", 50500)
