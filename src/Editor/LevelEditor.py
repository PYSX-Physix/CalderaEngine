import tkinter as tk
import pygame
import os

class LevelEditor:
    def __init__(self, project_path=None):
        self.project_dir = None
        self.root = tk.Tk()
        self.drawer_visable = False
        self.root.title("Caldera Engine")
        self.root.geometry("900x900")
        self.drawer = tk.Frame(self.root, )
        self.drawer.pack(side=tk.LEFT, fill=tk.Y, pady=10)
        self.toggle_button = tk.Button(self.root, text="Content Drawer",)
        self.content_label = tk.Label(self.drawer, text="Content")
        self.content_label.pack()
        self.project_list = tk.Listbox(self.drawer)
        self.project_list.pack(fill=tk.BOTH, expand=True)
        self.create_menubar()
        self.game_canvas_container = tk.Frame(self.root)
        self.game_canvas_container.pack(fill=tk.BOTH)
        if self.drawer_visable == False:
            self.drawer.pack_forget()
        else:
            self.drawer.pack(side=tk.LEFT, fill=tk.Y, padx=10)

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

        view_menu = tk.Menu(menubar, tearoff=0)
        view_menu.add_checkbutton(label="Content Drawer", command=self.toggle_content_drawer)
        menubar.add_cascade(label="View", menu=view_menu)

        self.root.config(menu=menubar)

    def toggle_content_drawer(self):
        if self.drawer_visable:
            self.drawer.pack_forget()
        else:
            self.drawer.pack(side=tk.LEFT, fill=tk.Y, padx=5)
        
        self.drawer_visable = not self.drawer_visable

    def create_content_drawer(self):
        print(f"Content Directory:")
