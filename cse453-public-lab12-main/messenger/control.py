########################################################################
# COMPONENT:
#    CONTROL
# Author:
#    Br. Helfrich, Kyle Mueller, Chandler Wright
# Summary: 
#    This class stores the notion of Bell-LaPadula
########################################################################

# you may need to put something here...

from enum import Enum

class Control(Enum):
    Public = 0
    Confidential = 1
    Privileged = 2
    Secret = 3

def readAccess(user_control_level, message_control_level):
    if user_control_level >= message_control_level:
        return True
    else:
        return False

def writeAccess(user_control_level, message_control_level):
    if user_control_level <= message_control_level:
        return True
    else:
        return False