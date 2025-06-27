This Project implements a fault-tolerant 2-phase commit (2PC) protocol with controlled and injected failures to understand the node crashes. It includes a transaction coordinator and multiple participants, running as separate process to simulate a distributed system.

Requirements:
 
Python 3.6 or later 
Download and install Python from the official website : https://www.python.org/downloads/


Structure:

Main.py            # Main program to run the 2PC protocol           
TxCoordinator.py   # Coordinator class to handle failures
Participants.py    # Participant class implementation for TC



Running the project:
 
Navigate to the directory where the Main.py of project is downloaded
Use the command prompt or terminal to run the Main.py file. 

Enter the following command:

> py Main.py

Select Options: 
After running the command, list of options displayed. These options represent different scenarios and their outcomes. Here are the available options:


	Enter your choice:
	1. Successful transaction with No Failures
	2. Coordinator fails before sending 'prepare' message
	3. Coordinator aborts after receiving 'NO' from Participant
	4. Coordinator fails after sending 'commit' message to the Participants
	5. Participant recovers after replying 'yes' to Coordinator
	6. EXIT
	

Choose an Option: 
Select the desired option from the list to simulate a specific failure case and observe its outcome between the Transaction Coordinator and Participants.

These steps will help you compile and run the program to analyze various failure scenarios in transaction handling.

Note : To verify all cases, you must exit the command prompt for the current case and then repeat the steps to verify the remaining cases.

