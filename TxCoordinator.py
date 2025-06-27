import time
import random
import threading
import socket

class Cordinator:
    def __init__(self) -> None: 
        self.thread_count = None                      # Initializing attributes
        self.participants = []
        self.transaction_id = random.randint(1, 10)   # random transaction ID between 1 and 10
        self.votes = False
        self.ack = False
        self.state = None
        self.timeout = 5
        self.FirstFailure = False
        self.ThirdFailure = False

    def First_Failure(self):                # Method to enable the first failure     
        self.FirstFailure = True

    def Third_Failure(self):            # Method to enable the third failure  
        self.ThirdFailure = True

    def add_participant(self, s_ip, s_port):   # Method to add participants to the coordinator
        self.participants.append((s_ip, s_port))
    
    def live(self):                      # Method to start the coordinator
        thread = threading.Thread(target=self.start)
        thread.start()

    def start_transaction(self):            # Method to initiate a transaction
        self.state = "INIT"
        print("Starting Transaction")
        print("Assigning Transaction ID: ", self.transaction_id)

    def stopping_transaction(self):          # Method to stop a transaction
        self.state = None
        print("Transaction stopped")
        self.stop()

    def start(self):       # Method representing the coordinator functions
        while True:
            time.sleep(2)
            if self.state is None:
                continue
            elif self.state == "INIT":
                self.send_broadcast()           # If state is "INIT", call send_broadcast
            elif self.state == "COMMIT":
                self.send_commit()              # If state is "COMMIT", call send_commit

#case 1
    def send_broadcast(self):        # Method to broadcast prepare message to participants
        time.sleep(4)
        self.votes = True
        threads = []
        self.thread_count = 0
        if self.FirstFailure:
            print("Transaction_Coordinator down!!! (before sending PREPARE)")
        for i in range(len(self.participants)):   # Broadcasting prepare message to all participants
            thread = threading.Thread(
                target=self.unicast_one_server, args=(self.participants[i], ))  # creating a new process for each participant 
            threads.append(thread)
            thread.start()

        while self.thread_count < len(self.participants):    # Waiting for all participants to respond
            time.sleep(5)

        if self.votes:                   # Determining the state based on participant votes
            self.state = "COMMIT"
        else:
            if self.FirstFailure:
                print("Transaction Aborted (Due to TC abort Initially)\n")
            else:
                print("Transaction Aborted (Due to No response from Node)\n")
            self.state = "ABORT"

    def unicast_one_server(self, participant):   # Method to send prepare message to a single participant
        ip, port = participant
        try:
            self.send_prepare(ip, port)
        except TimeoutError:
            self.votes = False

        self.thread_count += 1

    
    def send_prepare(self, ip, port):    # Method to send prepare message to a single participant
        send_socket = socket.socket()    
        send_socket.connect((ip, port))
        send_socket.send(f"{self.transaction_id}".encode())     # Sending transaction ID and receiving listening port
        port = send_socket.recv(1024).decode().strip()
        port = int(port)
        send_socket.close()
       
        if self.FirstFailure:    # Handling first failure scenario
            time.sleep(6)
            print(f"Participant '{port}' received notification that TC is up!!!")

        send_socket = socket.socket()
        send_socket.settimeout(5)
        send_socket.connect((ip, port))
        print(f"TC Successfully Sent PREPARE to Participant {port}")    # Sending prepare message and handling response
        send_socket.send(f"PREPARE;{str(self.transaction_id)}".encode())
        msg = send_socket.recv(1024).decode()
        print(f"TC received '{msg}' from Participant {port}")
        if msg == "no":
            self.votes = False
        send_socket.close()
#case 3
    def send_commit(self):      # Method to send commit message to all participants
        time.sleep(4)
        self.ack = True
        threads = []
        self.thread_count = 0
        for i in range(len(self.participants)):
            thread = threading.Thread(
                target=self.commit_unicast_single_server, args=(self.participants[i], ))
            threads.append(thread)
            thread.start()

            if i == 0 and self.ThirdFailure:            # Handling third failure scenario
                time.sleep(4)
                print("Transaction_Coordinator Down!!! (after sending 1 commit)")
                time.sleep(4)
                print("Transaction_Coordinator Up!!!")

       
        while self.thread_count < len(self.participants):    #Waiting for all participants to respond
            time.sleep(5)

        if self.ack:              #Determining the state based on participant acknowledgments
            self.state = None
            print("Transaction Completed")
        else:
            self.ack = "ABORT"

    def commit_unicast_single_server(self, participant): # Method to send commit message to a single participant
        ip, port = participant
        try:
            self.commit_prepare(ip, port)
        except TimeoutError:
            print("Timeout")

        self.thread_count += 1

    def commit_prepare(self, ip, port):    # Method to send commit message to a single participant
        send_socket = socket.socket()      # Establishing connection with participant
        send_socket.connect((ip, port))
        send_socket.send(f"{self.transaction_id}".encode())   # Sending transaction ID and receiving listening port
        port = send_socket.recv(1024).decode().strip()
        port = int(port)
        send_socket.close()
        send_socket = socket.socket()     # Establishing connection with participant
        send_socket.settimeout(5)
        send_socket.connect((ip, port))

        print(f"TC sends COMMIT to Participant {port}")   # Sending commit message and handling response
        send_socket.send(f"COMMIT;{str(self.transaction_id)}".encode())
        msg = send_socket.recv(1024).decode()
        print(f"TC receives '{msg}' from Participant {port}")
        if msg == "no":
            self.ack = False
        send_socket.close()
