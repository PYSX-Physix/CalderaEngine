from enum import Enum

class LogCategoryEnum(Enum):
    Error = "Error"
    Log = ""

def LogError(LogCategory: LogCategoryEnum, Message: str):
    print(f"{LogCategory}: {Message}")