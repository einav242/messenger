# from tkinter import *
#
#
# def click(user, address):
#     name = user.get()
#
#
# def close_window():
#     window.destroy()
#     exit()

def find_name(name: str):
    count = 0
    s = ''
    for i in range(len(name)):
        if count < 2:
            count += 1
            continue
        if name[i] == ":":
            break
        s = s + name[i]
        count += 1
    print(s)


if __name__ == '__main__':
    a="b'einav:'"
    find_name(a)
    # window = Tk()
    # # window.title("Client")
    # # window.configure(background="white")
    # # Label(window, text="username:", bg="white", fg="black",
    # #       font="none 12 bold").grid(row=1, column=0, sticky=W)
    # textentry1 = Entry(window, width=20, bg="white")
    # textentry1.grid(row=2, column=0, sticky=W)
    # Label(window, text="address:", bg="white", fg="black",
    #       font="none 12 bold").grid(row=3, column=0, sticky=W)
    # # textentry2 = Entry(window, width=20, bg="white")
    # # textentry2.grid(row=4, column=0, sticky=W)
    # # Label(window, text="", bg="white", fg="black", font="none 12 bold").grid(row=8, column=0, sticky=W)
    # # output = Text(window, width=75, height=5, wrap=WORD, background="white")
    # # output.grid(row=5, column=0, columnspan=2, sticky=W)
    # # # my_compdictionary = {'algorithm': 'step by step instruction to complete a task', 'bug': 'piece of code that causes'}
    # # # Label(window, text="click to exit:", bg="black", fg="white", font="none 12 bold").grid(row=6, column=0, sticky=W)
    # Button(window, text="Login", width=14, command=click(textentry1,textentry2)).grid(row=7, column=0, sticky=W)
    #
    # window.mainloop()
