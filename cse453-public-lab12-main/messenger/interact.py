########################################################################
# COMPONENT:
#    INTERACT
# Author:
#    Br. Helfrich, Kyle Mueller, Emilio Ordonez, Chandler Wright
# Summary: 
#    This class allows one user to interact with the system
########################################################################

import messages, control

###############################################################
# USER
# User has a name and a password
###############################################################
class User:
    def __init__(self, name, password, control):
        self.name = name
        self.password = password
        self.control = control

userlist = [
   [ "AdmiralAbe",     "password", control.Control.Secret ],  
   [ "CaptainCharlie", "password", control.Control.Privileged ], 
   [ "SeamanSam",      "password", control.Control.Confidential ],
   [ "SeamanSue",      "password", control.Control.Confidential ],
   [ "SeamanSly",      "password", control.Control.Confidential ]
]

###############################################################
# USERS
# All the users currently in the system
###############################################################
users = [*map(lambda u: User(*u), userlist)]

ID_INVALID = -1

######################################################
# INTERACT
# One user interacting with the system
######################################################
class Interact:

    ##################################################
    # INTERACT CONSTRUCTOR
    # Authenticate the user and get him/her all set up
    ##################################################
    def __init__(self, username, password, messages):
        self._authenticate(username, password)
        self._username = username
        self._p_messages = messages

    ##################################################
    # INTERACT :: SHOW
    # Show a single message
    ##################################################
    def show(self):
        id_ = self._prompt_for_id("display")
        self._p_messages.show(id_,self.control.value)
        print()

    ##################################################
    # INTERACT :: DISPLAY
    # Display the set of messages
    ################################################## 
    def display(self):
        print("Messages:")
        self._p_messages.display()
        print()

    ##################################################
    # INTERACT :: ADD
    # Add a single message
    ################################################## 
    def add(self):
        self._p_messages.add(self._prompt_for_line("message"),
                             self._username,
                             self._prompt_for_line("date"),
                             self._prompt_for_access_control())

    ##################################################
    # INTERACT :: UPDATE
    # Update a single message
    ################################################## 
    def update(self):
        id_ = self._prompt_for_id("update")
        self._p_messages.show(id_,self.control.value)
        self._p_messages.update(id_, self._prompt_for_line("message"))
        print()
            
    ##################################################
    # INTERACT :: REMOVE
    # Remove one message from the list
    ################################################## 
    def remove(self):
        self._p_messages.remove(self._prompt_for_id("delete"))

    ##################################################
    # INTERACT :: PROMPT FOR ACCESS CONTROL
    # Prompt for the access control
    ################################################## 
    def _prompt_for_access_control(self):
        print('Access control levels are as follows:')
        print('1: Public')
        print('2: Confidential')
        print('3: Privileged')
        print('4: Secret')

        choice = int(input('Enter the desired access control level number: '))
        
        # SOMEONE VALIDATE CHOICE

        while self.control.value > choice-1:
            print('Your clearance level is too high, please select one equal to or higher.')
            choice = int(input('Enter the desired access control level number: '))

        match choice:
            case 1:
                return control.Control.Public
            case 2:
                return control.Control.Confidential
            case 3:
                return control.Control.Privileged
            case 4:
                return control.Control.Secret

    ##################################################
    # INTERACT :: PROMPT FOR LINE
    # Prompt for a line of input
    ################################################## 
    def _prompt_for_line(self, verb):
        return input(f"Please provide a {verb}: ")

    ##################################################
    # INTERACT :: PROMPT FOR ID
    # Prompt for a message ID
    ################################################## 
    def _prompt_for_id(self, verb):
        return int(input(f"Select the message ID to {verb}: "))

    ##################################################
    # INTERACT :: AUTHENTICATE
    # Authenticate the user: find their control level
    ################################################## 
    def _authenticate(self, username, password):
        id_ = self._id_from_user(username)

        if id_ == -1:
            print('User is not in user list. You have been given public account access.')
            self.control = control.Control.Public
            return
        else:
            if password == users[id_].password:
                self.control = users[id_].control
            else:
                print('User is in user list, but the password is incorrect. You have been given public account access.')
                print('Restart the program to try again.')
                self.control = control.Control.Public
            return

    ##################################################
    # INTERACT :: ID FROM USER
    # Find the ID of a given user
    ################################################## 
    def _id_from_user(self, username):
        for id_user in range(len(users)):
            if username == users[id_user].name:
                return id_user
        return ID_INVALID

#####################################################
# INTERACT :: DISPLAY USERS
# Display the set of users in the system
#####################################################
def display_users():
    for user in users:
        print(f"\t{user.name}")
