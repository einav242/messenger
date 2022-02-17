import socket
import select

server = socket.socket()
server.bind(("192.168.1.101", 4434))
server.listen(5)
inputs = [server]
print("starting sever...")


def notify_all(msg, non_receptors):
    for connection in inputs:
        if connection not in non_receptors:
            connection.send(msg)


def greet(client):
    names = []
    for n in inputs:
        if n is not client and n is not server:
            names.append(n.getpeername())
    m = "hello user! \n users online: " + str(names)
    client.send(m.encode())


while inputs:
    readables, _, _ = select.select(inputs, [], [])
    for i in readables:
        if i is server:
            client, address = server.accept()
            inputs.append(client)
            print("connected to new client")
            greet(client)
            notify_all(f"client {address} enterd".encode(), [server, client])
        else:
            try:
                data=i.recv(1024)
                msg=str(str(i.getpeername()) + ">>> " + data.decode()).encode()
                notify_all(msg,[server,i])
            except Exception as e:
                print(e)
                inputs.remove(i)
                print(f"client {i.getpeername()} BYE")
                notify_all(f"client {i.getpeername()} left".encode(), [server])
                i.close()
