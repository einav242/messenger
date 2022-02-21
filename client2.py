import socket
import threading
from tkinter import *
import tkinter.scrolledtext
from tkinter import simpledialog


class client2:
    def __init__(self, host, port):
        self.users = []
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((host, port))
        self.msg = tkinter.Tk()
        self.msg.withdraw()
        self.nickname = simpledialog.askstring("Nickname", "please choose a nickname", parent=self.msg)
        print(self.nickname)
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
        self.win = tkinter.Tk()
        self.win.configure(bg="lightgray")

        self.name_label = tkinter.Label(self.win, text=self.nickname, bg="lightgray")
        self.name_label.config(font=("Ariel", 12))
        self.name_label.pack(padx=20, pady=5)

        self.start_button = tkinter.Button(self.win, text="start", command=self.write)
        self.start_button.config(font=("Ariel", 12))
        self.start_button.pack(padx=20, pady=5)

        self.chat_label = tkinter.Label(self.win, text="Chat:", bg="lightgray")
        self.chat_label.config(font=("Ariel", 12))
        self.chat_label.pack(padx=20, pady=5)

        self.text_area = tkinter.scrolledtext.ScrolledText(self.win)
        self.text_area.pack(padx=20, pady=5)
        self.text_area.config(state='disable')

        self.msg_label = tkinter.Label(self.win, text="Message:", bg="lightgray")
        self.msg_label.config(font=("Ariel", 12))
        self.msg_label.pack(padx=20, pady=5)

        self.input_area = tkinter.Text(self.win, height=3)
        self.input_area.pack(padx=20, pady=5)

        self.send_button = tkinter.Button(self.win, text="send all", command=self.write)
        self.send_button.config(font=("Ariel", 12))
        self.send_button.pack(padx=20, pady=5)

        self.sendto_area = tkinter.Text(self.win, height=1, width=20)
        self.sendto_area.pack(padx=20, pady=5)

        self.sendto_button = tkinter.Button(self.win, text="send to", command=self.write_to)
        self.sendto_button.config(font=("Ariel", 12))
        self.sendto_button.pack(padx=20, pady=5)

        # self.users_label = tkinter.Label(self.win, text="users:", bg="lightgray")
        # self.users_label.config(font=("Ariel", 12))
        # self.users_label.pack(padx=20, pady=5)
        #
        # self.users_area = tkinter.scrolledtext.ScrolledText(self.win)
        # self.users_area.pack(padx=20, pady=5)
        # self.users_area.config(state='disable')

        self.gui_done = True

        self.win.protocol("WM_DELETE_WINDOW", self.stop)

        self.win.mainloop()

    def write_to(self):
        name = self.sendto_area.get('1.0', 'end')
        message = f"{self.nickname}: {self.input_area.get('1.0', 'end')}"
        self.s.send(message.encode('utf-8'))
        self.sendto_area.delete('1.0', 'end')

    def write(self):
        message = f"{self.nickname}: {self.input_area.get('1.0', 'end')}"
        self.s.send(message.encode())
        self.input_area.delete('1.0', 'end')

    def stop2(self):
        self.running = False
        self.msg.destroy()
        self.s.close()
        exit(0)

    def stop(self):
        self.running = False
        self.win.destroy()
        self.s.close()
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
                m = message.split()[0]
                print(m)
                if message == 'NICK':
                    self.s.send(self.nickname.encode())
                else:
                    if self.gui_done:
                        self.text_area.config(state='normal')
                        self.text_area.insert('end', message)
                        self.text_area.yview('end')
                        self.text_area.config(state='disabled')
            except ConnectionAbortedError:
                break
            except:
                self.s.close()
                print("Error")
                exit(0)


client = client2("127.0.0.1", 9090)