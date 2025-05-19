import os
import sys

basepath = getattr(sys, '_MEIPASS', os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
print(f"Base path: {basepath}")

Project_JSON = os.path.join(basepath, "ProjectSelection", "Templates")