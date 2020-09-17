import socket, select, string, sys
import msvcrt
        
def prompt() :
    sys.stdout.write('<You> ')
    sys.stdout.flush()

def run_client(buffer=1024):
    
    # Require the passing of server address and port for connection
    assert len(sys.argv) == 3, "Server address and port are required for connection"   

    ADDRESS = sys.argv[1]
    PORT = int(sys.argv[2])
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
    
    # The client attempts to connect to the sever
    try :
        s.connect((ADDRESS, PORT))
    except :
        print(f'Connection Not Established on PORT: {PORT}, ADDRESS: {ADDRESS}\n Exiting Client')
        sys.exit()

    # Client prompts user for a name to be used in the chat room
    client_name = "Name:" + input("Client name: ")
    # Communication is sent to the server to indicate the user's name
    s.send(client_name.encode())
    print(f'Connection established to {ADDRESS} on port {PORT}')
    prompt()
    
    # Run client until interruption or disconnection
    while 1:
        sockets = [s]

        # Find compatible sockets for communications
        read_sockets, write_sockets, error_sockets = select.select(sockets , [], [], 1)
        # Check for any user keyboard input indicating a message
        # In case of input, append this input onto the read sockets
        if msvcrt.kbhit(): 
            read_sockets.append(sys.stdin)

        # Iterate over sockets checking for incoming and outgoing messages
        for sock in read_sockets:
            # Data from socket connected to server indicates an incoming communication
            if sock == s:
                data = sock.recv(buffer).decode()
                if not data :
                    # No data indicates a missed handshake with server signalling a disconnection
                    print('\nConnection to server lost')
                    sys.exit()
                else :
                    # Other data indicates a message, this is decoded and printed
                    sys.stdout.write(data)
                    prompt()
            
            # Otherwise, the next input is that of the user, this is then endoced and sent to the server
            else :
                msg = sys.stdin.readline()
                s.send(msg.encode())
                prompt()

#main function
if __name__ == "__main__":
    
    buffer = 1024

    # Require the passing of server address and port for connection
    assert len(sys.argv) == 3, "Server address and port are required for connection"   

    ADDRESS = sys.argv[1]
    PORT = int(sys.argv[2])
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
    
    # The client attempts to connect to the sever
    try :
        s.connect((ADDRESS, PORT))
    except :
        print(f'Connection Not Established on PORT: {PORT}, ADDRESS: {ADDRESS}\n Exiting Client')
        sys.exit()

    # Client prompts user for a name to be used in the chat room
    client_name = "Name:" + input("Client name: ")
    # Communication is sent to the server to indicate the user's name
    s.send(client_name.encode())
    print(f'Connection established to {ADDRESS} on port {PORT}')
    prompt()
    
    # Run client until interruption or disconnection
    while 1:
        sockets = [s]

        # Find compatible sockets for communications
        read_sockets, write_sockets, error_sockets = select.select(sockets , [], [], 1)
        # Check for any user keyboard input indicating a message
        # In case of input, append this input onto the read sockets
        if msvcrt.kbhit(): 
            read_sockets.append(sys.stdin)

        # Iterate over sockets checking for incoming and outgoing messages
        for sock in read_sockets:
            # Data from socket connected to server indicates an incoming communication
            if sock == s:
                data = sock.recv(buffer).decode()
                print(data)
                if not data :
                    # No data indicates a missed handshake with server signalling a disconnection
                    print('\nConnection to server lost')
                    sys.exit()
                else :
                    # Other data indicates a message, this is decoded and printed
                    sys.stdout.write(data)
                    prompt()
            
            # Otherwise, the next input is that of the user, this is then endoced and sent to the server
            else :
                msg = sys.stdin.readline()
                s.send(msg.encode())
                prompt()