import tkinter as tk
from tkinter import ttk, filedialog
import os
import json
from Shared.Paths import basepath
import subprocess

class ProjectWindow:
    def __init__(self):
        # Initialize the main window
        self.root = tk.Tk()
        self.root.title("Caldera Engine - Project Selector")
        self.root.geometry("900x800")
        # Loading layout
        self.project_category = ttk.Frame(self.root)
        self.project_category.pack(side=tk.TOP, fill=tk.BOTH)
        self.notebook = ttk.Notebook(self.project_category)
        # Create and load project frames
        self.create_project_frame = ttk.Frame(self.notebook)
        self.load_project_frame = ttk.Frame(self.notebook)
        self.create_project_frame.pack(fill=tk.BOTH, expand=True)
        self.load_project_frame.pack(fill=tk.BOTH, expand=True)
        self.info_box = ttk.Frame(self.create_project_frame)
        self.info_box.pack(fill=tk.BOTH, expand=True)
        self.create_buttons = ttk.Frame(self.create_project_frame)
        self.create_buttons.pack(fill=tk.X)
        self.create_notebook()
        # Create the layout for making projects
        self.create_project_layout()
        self.load_project_layout()
        self.list_projects()

        self.root.mainloop()

    def create_notebook(self):
        create_project_label = ttk.Label(self.create_project_frame, text="Create Project")
        load_project_label = ttk.Label(self.load_project_frame, text="Load Project")
        create_project_label.config(font=("Arial", 20, "bold"))
        load_project_label.config(font=("Arial", 20, "bold"))
        create_project_label.pack(side=tk.TOP, fill=tk.X)
        load_project_label.pack(side=tk.TOP, fill=tk.X)
        self.notebook.add(self.create_project_frame, text="Create Project")
        self.notebook.add(self.load_project_frame, text="Open Project")
        self.notebook.pack(fill=tk.BOTH, expand=True)

    def create_project_layout(self):
        self.project_name_container = ttk.Frame(self.create_project_frame)
        self.project_path_container = ttk.Frame(self.create_project_frame)
        self.project_path_label = ttk.Label(self.project_path_container, text="Project Path:  ")
        self.project_name_label = ttk.Label(self.project_name_container, text="Project Name:")
        self.project_name = ttk.Entry(self.project_name_container)
        self.project_path = ttk.Entry(self.project_path_container)
        self.project_path_selector = ttk.Button(self.project_path_container, text="...", command=self.set_project_path)
        self.create_button_container = ttk.Frame(self.create_project_frame)
        self.create_button_container.pack(side=tk.BOTTOM, fill=tk.X)
        self.cancel_button = ttk.Button(self.create_button_container, text="Cancel", command=self.root.destroy)
        self.cancel_button.pack(side=tk.LEFT, fill=tk.X)
        self.create_project_button = ttk.Button(self.create_button_container,text="Create Project", command=self.create_project)
        self.create_project_button.pack(side=tk.RIGHT, fill=tk.X)
        self.project_name_container.pack(fill=tk.X)
        self.project_path_container.pack(fill=tk.X)
        self.project_path_selector.pack(side=tk.RIGHT)
        self.project_path_label.pack(side=tk.LEFT)
        self.project_name_label.pack(side=tk.LEFT)
        self.project_name.pack(fill=tk.X)
        self.project_path.pack(fill=tk.X)

    def set_project_path(self):
        folder_dialog = filedialog.askdirectory(title="Set Project Path")
        if folder_dialog:
            self.project_path.delete(0, tk.END)
            self.project_path.insert(tk.END, folder_dialog)

    def load_project_layout(self):
        self.project_list = tk.Listbox(self.load_project_frame)
        self.project_list.bind("<Double-Button-1>", lambda event: self.load_project())
        self.project_list.pack(expand=True, fill=tk.BOTH)
        pass

    def load_project(self):
        """Loads project based on the user's selection."""
        selected_index = self.project_list.curselection()
        if not selected_index:  # No selection made
            print("Please select a project.")
            return

        selected_project = self.projects[selected_index[0]]  # Get project from JSON
        project_name = selected_project.get("project_name", "Unnamed Project")
        project_path = selected_project.get("project_path", "")

        if not project_path or not os.path.exists(project_path):
            print(f"Error: Project '{project_name}' has an invalid path.")
            return

        print(f"Loading project: {project_name} at {project_path}")

        # Open the project directory
        from Editor.LevelEditor import LevelEditor

        self.root.destroy()
        LevelEditor(project_path)


    def list_projects(self):
        """Loads projects from JSON and populates the list."""
        self.projects = []

        try:
            with open(os.path.join(basepath, "ProjectSelection", "projects.json"), "r") as file:
                self.projects = json.load(file)

            if not self.projects:
                self.project_list.insert(tk.END, "No saved projects found.")
                return

            for project in self.projects:
                project_name = project.get("project_name", "Unnamed Project")
                self.project_list.insert(tk.END, project_name)  # Only show project names

        except FileNotFoundError:
            self.project_list.insert(tk.END, "No projects found!")


    def create_project(self):
        """Creates a new project with directories and files."""
        project_name = self.project_name.get().strip()
        project_path = self.project_path.get().strip()

        if not project_name or not project_path:
            print("Please enter a valid project name and path.")
            return

        # Define target project directory
        target_dir = os.path.join(project_path, project_name)

        # Check if the directory already exists
        if os.path.exists(target_dir):
            print("Project directory already exists!")
            return

        # Create project directories
        directories = ["content", "config"]
        os.makedirs(target_dir, exist_ok=True)
        for directory in directories:
            os.makedirs(os.path.join(target_dir, directory), exist_ok=True)

        # Create blank files
        files = ["requirements.txt", "README.md", f"{project_name}.py"]
        for file in files:
            open(os.path.join(target_dir, file), "w").close()

        print(f"Project '{project_name}' created successfully at {target_dir}")

        from Editor.LevelEditor import LevelEditor
        LevelEditor(target_dir)
        self.root.destroy()
