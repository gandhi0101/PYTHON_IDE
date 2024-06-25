from enum import Enum
# Enum para representar los estados en el DFA del escáner
class StateType(Enum):
    Start = "Start"
    InAssign = "InAssign"
    InComment = "InComment"
    InMultiComment = "InMultiComment"
    InNum = "InNum"
    InReal = "InReal"
    InId = "InId"
    Done = "Done"
    EndFile = "EndFile"
