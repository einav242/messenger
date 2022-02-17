import socket
import select


class server:
    def __init__(self):
        self.server = socket.socket()
        self.server.bind(("192.168.1.101", 4434))
        self.server.listen(5)
        self.inputs = [self.server]
        print("starting sever...")
        while self.inputs:
            readables, _, _ = select.select(self.inputs, [], [])
            for i in readables:
                if i is self.server:
                    client, address = self.server.accept()
                    self.inputs.append(client)
                    print("connected to new client")
                    self.greet(client)
                    self.notify_all(f"client {address} enterd".encode(), [self.server, client])
                else:
                    try:
                        data = i.recv(1024)
                        msg = str(str(i.getpeername()) + ">>> " + data.decode()).encode()
                        self.notify_all(msg, [self.server, i])
                    except Exception as e:
                        print(e)
                        self.inputs.remove(i)
                        print(f"client {i.getpeername()} BYE")
                        self.notify_all(f"client {i.getpeername()} left".encode(), [self.server])
                        i.close()

    def notify_all(self, msg, non_receptors):
        for connection in self.inputs:
            if connection not in non_receptors:
                connection.send(msg)

    def greet(self, client):
        names = [n.getpeername() for n in self.inputs if n is not client and n is not self.server]
        m = "hello user! \n users online: " + str(names)
        client.send(m.encode())


server()
