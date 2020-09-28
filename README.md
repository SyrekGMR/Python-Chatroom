# Python-Chatroom
A simple python-based chatroom I made a while back whilst learning Python. 
<br>
To begin, you must first run server which will run on port 5000 and localhost by default.
```ruby
python Server.py
```
Next, run the client specifying the address and port number on which it is to connect.
```ruby
Python Client.py localhost 5000
```
<br><br>
The included code is heavily commented, explaining the functionality of each feature within the server and client files. The chatroom client works by establishing a handshake with the server and maintain this connection throughout a while loop.
<br>
<p align="center">
  <img src="Assets/Connected.png"/></img> 
</p>
The server consequently continues to listen for any communications from its connections, this looks at both the handshake verification and any data transmission. Upon receiving any encoded data from a connected client, the server then broadcasts this to all connected clients comprising the chat room, this communication is then displayed on the client's terminal. Any missed handshake between server and client indicates a disconnection in which case the server removes the client from its list of connections and broadcasts a disconnection message.
<br>
<p align="center">
  <img src="Assets/Disconnected.png"/></img>
</p>
