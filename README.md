# **:speech_balloon: Final Project - Messenger**

## This project is divided into 3️⃣ parts:
- **Part 1** – We built a primitive instant messaging system (similar to messenger) based on communication.
- **Part 2** – To the same system from part 1, we added a new layer (additional code) to transfer files over UDP.
- **Part 3** – We answered 9 questions (pdf attached) to the assignment.


### **To implement the project, we created a Server and a Client when:** 
The server initializes itself and "listens".
The server runs on a specific IP server and listens to clients in a specific port that known to sample clients for example: 50000,
when he allowing to connect to multiple clients at once (at least 5).
After a client disconnects the free port is returned to being a free resource.

Each customer can send a message to all connected chat and a private message to a specific connected person while monitoring the transfer using a TCP connection.
Each client can initiate a request to download a file from the server using a TCP connection in parallel with a file transfer channel by a UDP 
connection in order for the file transfer to be reliable and network load must be taken into account so we will implement FAST reliable UDP. 
finished, you receive an appropriate message and the last byte value sent.
The file can be downloaded simultaneously from several different clients. That is, 
it is possible that while waiting for permission to continue downloading from one client, 
the other client requests and starts receiving the file at the same time.


**The client :busts_in_silhouette: can perform the following operation:**
1. connect to server 
2. disconnect from server
3. Send a message to another customer
4. Sends a message to all clients currently connected to the server
5. Get the names of clients connected to the server
6. Get a list of files that exist on the server
7. Send a request to download a file from the server
8. download file from server

:bulb: Also, if a new customer has joined or disconnected an existing customer, an appropriate message must be sent to all participants.

It can be assumed that:
1. The number of messages per customer should not exceed 100 messages.
2. The maximum size per package (datagram) for UDP transfer is kB64 so it is 127.0.0.1 or localhost.

### **How to Run The Messenger:** 

### **The GUI:** 
**server:**
<img width="228" alt="Capture" src="https://user-images.githubusercontent.com/93201414/156808756-76684d99-726d-4e39-9c87-0342951a45b9.PNG">


