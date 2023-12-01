########################################################################
# COMPONENT:
#    CONTROL
# Author:
#    Br. Helfrich, Kyle Mueller, <your name here if you made a change>
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

userPermissions = { 
    "AdmiralAbe": Control.Secret,
    "CaptainCharlie": Control.Privileged,
    "SeamanSam": Control.Confidential,
    "SeamanSue": Control.Confidential,
    "SeamanSly": Control.Confidential,
    "Others": Control.Public
}