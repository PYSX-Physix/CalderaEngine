import tkinter as tk
import pygame

class CodeEditor:
    def __init__(self, filename=None, project_path=None):
        self.project_dir = None
        self.root = tk.Tk()
        self.root.title(f"Caldera Code Editor - {filename}")
        self.root.geometry("900x900")
        
        self.create_menubar()
        
        if project_path is None:
            print("No project is selected")
        else:
            print(f"Project path is: {project_path}")
            self.project_dir = project_path
        
        self.root.mainloop()

    def create_menubar(self):
        menubar = tk.Menu(self.root)

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
        edit_menu.add_command(label="Project Settings")
        edit_menu.add_command(label="Preferences")
        menubar.add_cascade(label="Edit", menu=edit_menu)

    def create_texteditor(self):
        self.text_editor = tk.Text(self.root, wrap=tk.WORD)
        self.text_editor.pack(fill=tk.BOTH, expand=True)
        self.text_editor.focus_set()
        if self.filename:
            with open(self.filename, 'r') as file:
                self.text_editor.insert(tk.END, file.read())
        else:
            self.text_editor.insert(tk.END, "// Start coding here...")