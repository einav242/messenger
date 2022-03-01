# **Final Project - Messenger**

## This project is divided into 3️⃣ parts:
- **Part 1** – We have built a primitive instant messaging system (similar to messenger) based on communication.
- **Part 2** – For the same Class A system, we added a new layer (additional code) to transfer files over UDP.
- **Part 3** – We answered 9 questions (pdf attached) to the assignment.


### **For the purpose of implementing the project, we created a Server and a Client when:** 
The server initializes itself and "listens".
The server runs on a particular IP server and listens to clients in a particular port known to sample clients 50000,
allowing it to connect to multiple clients at once (at least 5).
After a client disconnects the free port is returned to being a free resource.

Each customer can send a message to all connected chat and a private message to a specific connected person while monitoring the transfer using a TCP connection.
Each client can initiate a request to download a file from the server using a TCP connection in parallel with a file transfer channel by a UDP 
connection in order for the file transfer to be reliable and network load must be taken into account so we will implement FAST reliable UDP. 
finished, you receive an appropriate message and the last byte value sent.
The file can be downloaded simultaneously from several different clients. That is, 
it is possible that while waiting for permission to continue downloading from one client, 
the other client requests and starts receiving the file at the same time.


**The client can perform the following operation:**
1. connect to server 
2. disconnect from server
3. Send a message to another customer
4. Sends a message to all clients currently connected to the server
5. Get the names of clients connected to the server
6. Get a list of files that exist on the server
7. Send a request to download a file from the server
8. download file from server

Also, if a new customer has joined or disconnected an existing customer, an appropriate message must be sent to all participants.

It can be assumed that:
1. The number of messages per customer should not exceed 100 messages.
2. The maximum size per package (datagram) for UDP transfer is kB64 so it is 127.0.0.1 or localhost.

### **How to Run The Messenger:** 

