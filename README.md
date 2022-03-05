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

### **How to Run The System:** 
First we will run the server through the CMD By writing the line:<br />
`python3 Server.py` <br />
The file server.py is in the folder server.
and the next window will open:<br />

<img width="500" alt="Capture" src="https://user-images.githubusercontent.com/93201414/156808756-76684d99-726d-4e39-9c87-0342951a45b9.PNG">

Now the client can be added to the system
To add a client we will write the next line in CMD:<br />
`python3 Client.py`<br />
Immediately, a window will pop up where we write down what nickname we want:<br />

<img width="400" alt="Capture1" src="https://user-images.githubusercontent.com/93201414/156809927-17d6ad70-3b81-4e99-8e2b-4df4746e76c7.PNG">

After we chose a nickname, we clicked OK.

The chat window now opens To connect to the server, we click Start.<br />
<img width="500" alt="Captursasae" src="https://user-images.githubusercontent.com/93201414/156886749-a777e374-1a9e-4dd8-91e9-24c470c7c71c.PNG"><br />


**Server:**<br />
To disconnect from the server, click a button: **log out**

**Actions that the client can perform:**<br />
1. Show the names of the clients Online by clicking the button: **Show Online**
2. Show the files on the server by clicking the button: **Show Srever File**
3. Send a message to everyone in the group by writing the message **&** pressing a button: **Send all**
4. Send a private message by writing the message **&** the name of the customer you want to send to in the pane: **To**,<br />
**&** pressing a button: **Send private**
5. Download a file 
6. To disconnect from the server, click the button: **Log Out**

If you choose to download a document, during the process you will open the following window:<br />
<img width="500" alt="Captfure" src="https://user-images.githubusercontent.com/93201414/156887016-0adf1c0c-a251-4fba-9414-8944c258f161.PNG">

You can choose whether to continue downloading the document or stop the download process

You can see that our system allows two customers to download the same file at the same time without a problem 

<img width="991" alt="Capture540943" src="https://user-images.githubusercontent.com/93201414/156889173-4c69e48d-2dd6-4d15-bf2b-0a178be88432.PNG">


### **Diagram depicting our project:** 

<p align="center" width="100%"><img width="500" alt="Capture58478943" src="https://user-images.githubusercontent.com/93201414/156886385-a5bdb531-31ae-4e4d-a16a-865e28a152aa.PNG">


