import tkinter as tk
import pygame
import os

class LevelEditor:
    def __init__(self, project_path=None):
        self.project_dir = None
        self.root = tk.Tk()
        self.root.title("Caldera Engine")
        self.root.geometry("900x900")
        self.create_menubar()
        self.game_canvas_container = tk.Frame(self.root)
        self.game_canvas_container.pack(fill=tk.BOTH)
        if project_path == None:
            print("No project is selected")
        elif project_path != None:
            print(f"Project path is: {project_path}")
            self.project_dir = project_path
        self.root.mainloop()

    def create_menubar(self):
        menubar=tk.Menu(self.root)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Open", accelerator="Cmd+O")
        file_menu.add_command(label="Save", accelerator="Cmd+S")
        menubar.add_cascade(label="File", menu=file_menu)

        edit_menu = tk.Menu(menubar, tearoff=0)
        edit_menu.add_command(label="Project Settings")
        edit_menu.add_command(label="Preferences")
        menubar.add_cascade(label="Edit", menu=edit_menu)

        self.root.config(menu=menubar)

    
