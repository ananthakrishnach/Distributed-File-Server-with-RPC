import time
import socket       #importing the socket

class Participant:
    def __init__(self, participant_id, ip, port):
        self.socket = None
        self.listen_socket = None
        self.node_failure = False  # Flag to node failure
        self.failure= False  # Flag to failure case 4
        self.participant_id = participant_id
        self.ip = ip
        self.port = port
        self.l_port = port + 1  # Listening port
        self.vote = "yes"  
        self.transaction_info = None  # Transaction information
 #case 4
    def failure4(self):                 # Method to enable failure case 4
        self.failure = True
  #case 2  
    def participant_down(self):       # Method to simulate participant going down
        self.node_failure = True
  
    def live(self):                   # Method to start participant's operation
        self.socket = socket.socket()              #creating socket object to set up main socket
        self.socket.bind((self.ip, self.port))      # Binding the socket to IP add and port
        self.socket.listen(5)

        while True:
            connection, address = self.socket.accept()
            self.transaction_info = connection.recv(1024).decode()
            connection.send(f"{self.l_port}".encode())

            self.listen_socket = socket.socket()         # Setting up the listening socket
            try:
                self.listen_socket.bind((self.ip, self.l_port))
                self.listen_socket.listen(1)            # setting listen socket to listen incoming connections 
                self.listen_socket.settimeout(5)        # setting a timeout of 5 seconds for accepting connections

                connection, address = self.listen_socket.accept()      # To accept incoming conenctions 
                message = connection.recv(1024).decode()
                msg, self.transaction_info = message.split(';')
                print(f"Participant {self.port} receives {msg} from TC")  #printing the received message

                
                if self.node_failure:      # To enable node failure
                    time.sleep(4)
                    print(f"Participant '{self.port}' Down!!!")
                    time.sleep(4)
                
                if self.failure:         # To enable failure case 4
                    print(f"Participant '{self.port}' Down!!!")
                    time.sleep(4)
                    print(f"Participant '{self.port}' UP!!!")
                    print(f"Participant '{self.port}' fetched transaction ID(from TC): {self.transaction_info}")

                if msg == "PREPARE":           # Handling different messages from TC
                    connection.send(self.vote.encode())
                elif msg == "COMMIT":
                    connection.send("ACK".encode())
            except TimeoutError:
                print(f"Participant '{self.port}' aborted")
                self.listen_socket.settimeout(None)
                connection, address = self.listen_socket.accept()
                message = connection.recv(1024).decode()
                msg, self.transaction_info = message.split(';')
                self.vote = "no"
                print(f"Participant {self.port} received {msg} from TC")

                if self.node_failure:         #To enable node failure
                    time.sleep(4)
                    print(f"Participant '{self.port}' Down!!!")
                    time.sleep(4)
                

                if msg == "PREPARE":           # Handling different messages from TC
                    connection.send(self.vote.encode())
                elif msg == "COMMIT":
                    connection.send("ACK".encode())

            self.listen_socket.close()     #closing the connection
