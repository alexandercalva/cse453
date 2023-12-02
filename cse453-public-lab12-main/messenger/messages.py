################################################################################
# COMPONENT:
#    MESSAGES
# Author:
#    Br. Helfrich, Kyle Mueller, Emilio Ordonez, Chandler Wright, John Stennett
# Summary: 
#    This class stores the notion of a collection of messages
################################################################################

import control, message

##################################################
# MESSAGES
# The collection of high-tech messages
##################################################
class Messages:

    ##################################################
    # MESSAGES CONSTRUCTOR
    # Read a file to fill the messages
    ##################################################
    def __init__(self, filename):
        self._messages = []
        self._read_messages(filename)

    ##################################################
    # MESSAGES :: DISPLAY
    # Display the list of messages
    ################################################## 
    def display(self):
        for m in self._messages:
            m.display_properties()

    ##################################################
    # MESSAGES :: SHOW
    # Show a single message
    ################################################## 
    def show(self, id, userControlLevel):
        doesNotExist = True
        existsNotCleared = True
        for m in self._messages:
            if m.get_id() == id:
                doesNotExist = False
                if control.readAccess(userControlLevel, m._text_control.value):
                    existsNotCleared = False
                    m.display_text()

        if doesNotExist:
            print('Message doesnt exist.')
            existsNotCleared = False
        if existsNotCleared:
            print('You do not have clearance to read.')

    ##################################################
    # MESSAGES :: UPDATE
    # Update a single message
    ################################################## 
    def update(self, id, userControlLevel, text):
        for m in self._messages:
            if m.get_id() == id:
                if control.writeAccess(userControlLevel, m._text_control.value):
                    m.update_text(text)
                else:
                    print("Your clearance is too high to write to this message.")

    ##################################################
    # MESSAGES :: REMOVE
    # Remove a single message
    ################################################## 
    def remove(self, id, userControlLevel):
        for m in self._messages:
            if m.get_id() == id:
                if control.readAccess(userControlLevel, m._text_control.value):
                    m.clear()
                else:
                    print('You do not have clearance to delete this message.')

    ##################################################
    # MESSAGES :: ADD
    # Add a new message
    ################################################## 
    def add(self, text, author, date, text_control):
        m = message.Message(text, author, date, text_control)
        self._messages.append(m)

    ##################################################
    # MESSAGES :: READ MESSAGES
    # Read messages from a file
    ################################################## 
    def _read_messages(self, filename):
        try:
            with open(filename, "r") as f:
                for line in f:
                    text_control, author, date, text = line.split('|')
                    match text_control:
                        case "Secret":
                            text_control = control.Control.Secret
                        case "Confidential":
                            text_control = control.Control.Confidential
                        case "Public":
                            text_control = control.Control.Public
                        case "Privileged":
                            text_control = control.Control.Privileged
                    self.add(text.rstrip('\r\n'), author, date, text_control)

        except FileNotFoundError:
            print(f"ERROR! Unable to open file \"{filename}\"")
            return
