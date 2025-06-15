from ProjectSelection.ProjectWindow import ProjectWindow
from Editor.LevelEditor import LevelEditor

class CalderaEngine():
    def __init__(self, project_path="/Users/gunnargibbens/Desktop/Caldera_Game"):
        if project_path:
            self.editor = LevelEditor(project_path)
        else:
            ProjectWindow()

if __name__ == "__main__":
    CalderaEngine()