from Participants import Participant   #importing the coordinator and participant 
from TxCoordinator import Cordinator
import threading


def live_participant(participant, down=False, failure4=False):    # Function for live participant behavior
    if down:
        participant.participant_down()  # if participant failure
    if failure4:
        participant.failure4()  # in failure case 4
    participant.live()  # Participant goes live


def successful_transaction(participants, participants_ports):    # Function for successful transaction
    threads_no_failure = []                                      #list to store threads for each participant 
    for i in range(len(participants_ports)):
        thread = threading.Thread(target=live_participant, args=(participants[i],))  #creating new thread
        threads_no_failure.append(thread)
        thread.start()  # starting thread
    tc.live()
    tc.start_transaction()  #starting transcation


def failure1(participants, participants_ports):   # Function for TC failure before sending 'prepare' message
    threads_failure1 = [] 
    for i in range(len(participants_ports)):
        thread = threading.Thread(target=live_participant, args=(participants[i],))
        threads_failure1.append(thread)
        thread.start()
    tc.First_Failure()
    tc.live()
    tc.start_transaction()


def failure2(participants, participants_ports): # Function for node failure before sending 'yes' to TC
    threads_failure2 = []
    for i in range(len(participants_ports)):
        thread = threading.Thread(target=live_participant, args=(participants[i], True if i == 0 else False))
        threads_failure2.append(thread)
        thread.start()
    tc.live()
    tc.start_transaction()
1

def failure3(participants, participants_ports):  # Function for TC failure after sending one 'commit' message
    threads_failure3 = []
    for i in range(len(participants_ports)):
        thread = threading.Thread(target=live_participant, args=(participants[i],))
        threads_failure3.append(thread)
        thread.start()
    tc.Third_Failure()
    tc.live()
    tc.start_transaction()


def failure4(participants, participants_ports):   # Function for node failure after replying 'yes' to TC
    threads_failure4 = []
    for i in range(len(participants_ports)):
        thread = threading.Thread(target=live_participant, args=(participants[i], False, True if i == 0 else False))
        threads_failure4.append(thread)
        thread.start()
    tc.live()
    tc.start_transaction()

def options():          # Function to display menu options
    print("Enter your choice:")
    print("1. Successful transaction with No Failures")
    print("2. Coordinator fails before sending 'prepare' message")
    print("3. Coordinator aborts after receiving 'NO' from Participant")
    print("4. Coordinator fails after sending 'commit' message to the Participants")
    print("5. Participant recovers after replying 'yes' to Coordinator")
    print("6. EXIT")

if __name__ == '__main__':        #main block
    tc = Cordinator()
    participants = []              #an empty list to store participants
    participants_ports = [1801, 1901]   # 2 ports for participants

    
    for i in range(len(participants_ports)):          # Creating participants and adding to coordinator
        s_ip = 'localhost'                            # IP add for participants
        s_port = participants_ports[i]
        s_id = i + 1

        new_server = Participant(s_id, s_ip, s_port)   # Creating new participant instances
        participants.append(new_server)        #to add participants to the list 
        tc.add_participant(s_ip, s_port)

    options()
    choice = input()   #input from the user
    if choice == '1':
        successful_transaction(participants, participants_ports)
    elif choice == '2':
        failure1(participants, participants_ports)
    elif choice == '3':
        failure2(participants, participants_ports)
    elif choice == '4':
        failure3(participants, participants_ports)
    elif choice == '5':
        failure4(participants, participants_ports)
    elif choice == '6':
        print("Exiting...")
    else:
        print("\nInvalid Input. Please select a valid option.\n")
