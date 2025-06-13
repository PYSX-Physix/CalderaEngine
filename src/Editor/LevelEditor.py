import tkinter as tk
from Editor.ProjectSettings import ProjectSettings
import pygame
import os

class LevelEditor:
    def __init__(self, project_path=None):
        self.project_dir = None
        self.root = tk.Tk()
        self.drawer_visable = False
        self.root.title("Caldera Engine")
        self.root.geometry("900x900")
        self.drawer = tk.Frame(self.root)
        self.drawer.pack(side=tk.LEFT, fill=tk.Y, pady=10)
        self.toolbar = tk.Frame(self.drawer)
        self.toolbar.pack(fill=tk.X, padx=5, pady=(5, 0))
        self.add_file_button = tk.Button(self.toolbar, text="Add File", command=self.add_file)
        self.add_file_button.pack(side=tk.LEFT, padx=2)
        self.add_folder_button = tk.Button(self.toolbar, text="Add Folder", command=self.add_folder)
        self.add_folder_button.pack(side=tk.LEFT, padx=2)
        self.content_label = tk.Label(self.drawer, text="Content")
        self.content_label.pack()
        self.project_list = tk.Listbox(self.drawer)
        self.project_list.pack(fill=tk.BOTH, expand=True)
        self.create_menubar()
        self.game_canvas_container = tk.Frame(self.root)
        self.game_canvas_container.pack(fill=tk.BOTH)
        self.toggle_button_container = tk.Frame(self.root)
        self.toggle_button_container.pack(side=tk.BOTTOM, fill=tk.X, pady=5)
        self.toggle_button = tk.Button(self.toggle_button_container, text="Content Drawer", command=self.toggle_content_drawer)
        self.toggle_button.pack(side=tk.LEFT, padx=5)
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
        edit_menu.add_command(label="Undo", accelerator="Cmd+Z")
        edit_menu.add_command(label="Redo", accelerator="Cmd+Y")
        edit_menu.add_command(label="Cut", accelerator="Cmd+X")
        edit_menu.add_command(label="Copy", accelerator="Cmd+C")
        edit_menu.add_command(label="Paste", accelerator="Cmd+V")
        edit_menu.add_separator()
        edit_menu.add_command(label="Project Settings", command=self.open_project_settings)
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
            self.create_content_drawer()  # Refresh content when shown
        
        self.drawer_visable = not self.drawer_visable

    def create_content_drawer(self):
        # Clear the listbox first
        self.project_list.delete(0, tk.END)
        if self.project_dir:
            content_dir = os.path.join(self.project_dir, "content")
            if os.path.isdir(content_dir):
                files = os.listdir(content_dir)
                for f in files:
                    self.project_list.insert(tk.END, f)
            else:
                self.project_list.insert(tk.END, "No 'content' folder found.")
        else:
            self.project_list.insert(tk.END, "No project loaded.")

    def add_file(self):
        # Simple file creation dialog
        import tkinter.simpledialog
        filename = tk.simpledialog.askstring("Add File", "Enter new file name:")
        if filename and self.project_dir:
            content_dir = os.path.join(self.project_dir, "content")
            os.makedirs(content_dir, exist_ok=True)
            file_path = os.path.join(content_dir, filename)
            if not os.path.exists(file_path):
                with open(file_path, "w") as f:
                    f.write("")  # Create empty file
                self.create_content_drawer()
            else:
                tk.messagebox.showerror("Error", "File already exists.")

    def add_folder(self):
        # Simple folder creation dialog
        import tkinter.simpledialog
        foldername = tk.simpledialog.askstring("Add Folder", "Enter new folder name:")
        if foldername and self.project_dir:
            content_dir = os.path.join(self.project_dir, "content")
            os.makedirs(content_dir, exist_ok=True)
            folder_path = os.path.join(content_dir, foldername)
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
                self.create_content_drawer()
            else:
                tk.messagebox.showerror("Error", "Folder already exists.")

    def open_code_editor(self, filename=None):
        # Placeholder for opening code editor
        from Editor.CodeEditor import CodeEditor
        CodeEditor(filename, self.project_dir)

    def open_project_settings(self):
        # Placeholder for opening project settings
        ProjectSettings()