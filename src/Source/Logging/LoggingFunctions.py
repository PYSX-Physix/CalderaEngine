from enum import Enum

class LogCategoryEnum(Enum):
    Error = "Error"
    Log = "Log"

COLORS = {
    LogCategoryEnum.Error: "\033[91m",
    LogCategoryEnum.Log: "\033[94m",
}
RESET = "\033[0m"

def PrintToLogs(LogCategory: LogCategoryEnum, Message: str):
    color = COLORS.get(LogCategory, "")
    print(f"{color}{LogCategory.value}: {Message}{RESET}")