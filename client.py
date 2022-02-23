import socket
import threading
from tkinter import *
import tkinter.scrolledtext
from tkinter import simpledialog


class client:
    def __init__(self, host, port):
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
        self.win.configure(background="white")

        Button(self.win, text="start", width=12, command=self.write).grid(row=0, column=0, sticky=W)
        Label(self.win, text="name:" + self.nickname + "  address:" + str(self.s.getpeername()), bg="white", fg="black",
              font="none 12 bold").grid(row=0, column=1, sticky=W)

        Button(self.win, text="Show Online", width=12, command=self.user_list).grid(row=0, column=2, sticky=W)
        Button(self.win, text="Show Server Files", width=12, command=None).grid(row=2, column=2, sticky=W)

        Label(self.win, text="Chat:", bg="white", fg="black", font="none 12 bold").grid(row=3, column=1, sticky=W)
        self.input_area = Text(self.win, width=75, height=15, wrap=WORD, background="lightgray")
        self.input_area.grid(row=5, column=0, columnspan=2, sticky=W)

        Label(self.win, text="Message:", bg="white", fg="black", font="none 12 bold").grid(row=6, column=0, sticky=W)
        self.msg = Entry(self.win, width=40, bg="white")
        self.msg.grid(row=7, column=0, sticky=W)
        Button(self.win, text="Send all", width=12, command=self.write).grid(row=7, column=1, sticky=W)
        Label(self.win, text="To:", bg="white", fg="black", font="none 12 bold").grid(row=8, column=0, sticky=W)
        self.user = Entry(self.win, width=40, bg="white")
        self.user.grid(row=9, column=0, sticky=W)
        Button(self.win, text="Send private", width=12, command=self.write_to).grid(row=9, column=1, sticky=W)

        Label(self.win, text="Server File Name:", bg="white", fg="black", font="none 12 bold").grid(row=10, column=0,
                                                                                                    sticky=W)
        self.file = Entry(self.win, width=40, bg="white")
        self.file.grid(row=11, column=0, sticky=W)
        Label(self.win, text="Save as:", bg="white", fg="black", font="none 12 bold").grid(row=10, column=1,
                                                                                           sticky=W)
        self.file_save = Entry(self.win, width=40, bg="white")
        self.file_save.grid(row=11, column=1, sticky=W)
        Button(self.win, text="Download", width=12, command=self.download).grid(row=11, column=2, sticky=W)

        Button(self.win, text="Log Out", width=12, command=self.stop).grid(row=12, column=0, sticky=W)
        self.gui_done = True

        self.win.protocol("WM_DELETE_WINDOW", self.stop)

        self.win.mainloop()

    def download(self):
        self.soc = socket.socket()
        self.soc.connect(("127.0.0.1", 1234))
        message = self.file.get()
        file_save = self.file_save.get()
        self.soc.send(message.encode())
        self.file.delete(0, END)
        self.soc.close()


    def user_list(self):
        message = "send1234"
        self.s.send(message.encode())

    def write_to(self):
        name = self.user.get()
        message = f"private {name} {self.nickname}: {self.msg.get()}" + "\n"
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
        self.soc.close()

        exit(0)

    def start(self):
        message = self.s.recv(1024)

        self.users_area.config(state='normal')
        self.users_area.insert('end', message)
        self.users_area.yview('end')
        self.users_area.config(state='disabled')

    def receive(self):
        while self.running:
            try:
                message = self.s.recv(1024)
                if message == 'NICK':
                    self.s.send(self.nickname.encode())
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
