import socket
import select


def run_server(buffer=1024, address="0.0.0.0"):
     connections = []
     RECV_BUFFER = buffer # Size of message buffer to be sent through the server
     ADDRESS = address # Address for server, "" will result in the localhost being used, for use on local network use that network's ip
     PORT = 5000 # Port number for routing, the port number is largerly arbitrary
     

     server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
     server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 2)
     # Server binds to given address and port and begins listening for incoming calls
     server_socket.bind((ADDRESS, PORT))
     server_socket.listen(10)
     connections.append(server_socket)

     print("Server initisalised on port " + str(PORT))
     
     clients = {}

     # Run server until keyboard interrupt
     while 1:
          # Continually check list of sockets for incoming data
          read_sockets,write_sockets,error_sockets = select.select(connections,[],[])
          for sock in read_sockets:
               #A comminications from the server sockets indicates a new connection
               if sock == server_socket:
                # New connection is appended onto list of connection and a communication is sent out from the server informin of this new connection
                    sockfd, addr = server_socket.accept()
                    connections.append(sockfd)
                    print("User (%s, %s) has connected" % addr)
                    # Data sent over the server must first be encoded using .encode()
                    broadcast(sockfd, ("[%s:%s] has entered the chat room\n" % addr).encode(), connections, server_socket)
               
               #Communications from other sockets indicate messages from other clients
               else:
                    try:
                         # Try processing incoming data
                         data = sock.recv(RECV_BUFFER).decode()
                         # Initial communication from client will tell the server the client's name to be used with each message
                         # Name can be later change by sending the name prefixed with "Name: "
                         if data[:5] == "Name:":
                              clients[str(sock.getpeername())] = data[5:]
                         # Subsequent communcation are assumed to be messages
                         elif data:
                              broadcast(sock, ("\r" + '<' + clients[str(sock.getpeername())] + '>  ' + data, connections, server_sock).encode())
                    
                    except:
                         # Otherwise, the client has disconnected
                         # The server communicates the disconnection to all clients
                         broadcast(sock, "Client (%s, %s) is offline" % addr, connections, server_socket)
                         print("Client (%s, %s) is offline" % addr)
                         # Disconnected client's socket is closed
                         sock.close()
                         connections.remove(sock)
                         continue
     
     server_socket.close()

def broadcast (sock, message, connections, server_sock):
     #Do not send the message to master socket and the client who has send us the message
     for socket in connections:
          if socket != server_sock and socket != sock :
               try :
                    socket.send(message)
               except :
                    # broken socket connection may be, chat client pressed ctrl+c for example
                    socket.close()
                    connections.remove(socket)

if __name__ == "__main__":
     
     buffer=1024
     address="0.0.0.0"

     connections = []
     RECV_BUFFER = buffer # Size of message buffer to be sent through the server
     ADDRESS = address # Address for server, "" will result in the localhost being used, for use on local network use that network's ip
     PORT = 5000 # Port number for routing, the port number is largerly arbitrary
     

     server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
     server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 2)
     # Server binds to given address and port and begins listening for incoming calls
     server_socket.bind((ADDRESS, PORT))
     server_socket.listen(10)
     connections.append(server_socket)

     print("Server initisalised on port " + str(PORT))
     
     clients = {}

     # Run server until keyboard interrupt
     while 1:
          # Continually check list of sockets for incoming data
          read_sockets,write_sockets,error_sockets = select.select(connections,[],[],)
          for sock in read_sockets:
               #A comminications from the server sockets indicates a new connection
               if sock == server_socket:
                # New connection is appended onto list of connection and a communication is sent out from the server informin of this new connection
                    sockfd, addr = server_socket.accept()
                    connections.append(sockfd)
                    print("User (%s, %s) has connected" % addr)
                    # Data sent over the server must first be encoded using .encode()
                    broadcast(sockfd, ("[%s:%s] has entered the chat room\n" % addr).encode(), connections, server_socket)
               
               #Communications from other sockets indicate messages from other clients
               else:
                    try:
                         # Try processing incoming data
                         data = sock.recv(RECV_BUFFER).decode()
                         # Initial communication from client will tell the server the client's name to be used with each message
                         # Name can be later change by sending the name prefixed with "Name: "
                         if data[:5] == "Name:":
                              clients[str(sock.getpeername())] = data[5:]
                         # Subsequent communcation are assumed to be messages
                         elif data:
                              broadcast(sock, ("\r" + '<' + clients[str(sock.getpeername())] + '>  ' + data).encode())
                    
                    except:
                         # Otherwise, the client has disconnected
                         # The server communicates the disconnection to all clients
                         broadcast(sock, "Client (%s, %s) is offline" % addr, connections, server_socket)
                         print("Client (%s, %s) has disconnected" % addr)
                         # Disconnected client's socket is closed
                         sock.close()
                         connections.remove(sock)
                         continue
     
     server_socket.close()