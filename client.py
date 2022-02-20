import socket
import threading
from tkinter import *


class client:
    def __init__(self):
        self.window = None
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect(("127.0.0.1", 4434))
        # t = threading.Thread(target=self.send)
        # t.start()
        t2 = threading.Thread(target=self.rec)
        t2.start()
        t3 = threading.Thread(target=self.draw)
        t3.start()

    def rec(self):
        while True:
            try:
                print(self.s.recv(1024).decode())
            except:
                pass

    def send_to(self, msg):
        # while True:
        try:
            self.s.send(msg.get())
        except:
            print("hi")

    def temp(self, msg):
        self.s.send(msg.get().encode())
        # msg.delete(0.0, END)

    def draw(self):
        self.window = Tk()
        self.window.title("client")
        self.window.configure(background="white")
        Label(self.window, text="                                                                 ", bg="white",
              fg="black", font="none 12 bold").grid(row=1, column=5, sticky=W)
        Label(self.window, text="message: ", bg="white", fg="black",
              font="none 12 bold").grid(row=1, column=0, sticky=W)
        textentry1 = Entry(self.window, width=50, bg="white")
        textentry1.grid(row=2, column=0, sticky=W)
        msg = textentry1.get()
        Button(self.window, text="send all", width=14, command=self.temp(textentry1)).grid(row=7, column=0, sticky=W)
        self.window.mainloop()


client()
