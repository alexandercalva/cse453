########################################################################
# COMPONENT:
#    CONTROL
# Author:
#    Br. Helfrich, Kyle Mueller, Chandler Wright
# Summary: 
#    This class stores the notion of Bell-LaPadula
########################################################################

 
 ######################################################
# Control Enum
# This Enum controls the different access levels for both users and messages
######################################################

from enum import Enum

class Control(Enum):
    Public = 0
    Confidential = 1
    Privileged = 2
    Secret = 3

 ######################################################
# readAccess
# Returns a Boolean depending on if the user has a high enough
# clearance to read the message.
######################################################

def readAccess(user_control_level, message_control_level):
    if user_control_level >= message_control_level:
        return True
    else:
        return False

 ######################################################
# writeAccess
# Returns a Boolean depending on if the user has a high enough
# clearance to write to the message.
######################################################

def writeAccess(user_control_level, message_control_level):
    if user_control_level <= message_control_level:
        return True
    else:
        return False