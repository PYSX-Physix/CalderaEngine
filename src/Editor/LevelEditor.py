import tkinter as tk
from tkinter import ttk
from Source.Logging.LoggingFunctions import PrintToLogs, LogCategoryEnum as LogType
from Editor.Settings.ProjectSettings import ProjectSettings
from Editor.Settings.EditorSettings import EditorSettingsWindow
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

        # Use Treeview for hierarchical content
        self.project_tree = ttk.Treeview(self.drawer)
        self.project_tree.pack(fill=tk.BOTH, expand=True)
        self.project_tree.heading("#0", text="Project Content", anchor='w')
        self.project_tree.bind("<Double-1>", self.on_tree_double_click)
        self.project_tree.bind("<Button-2>", self.on_tree_right_click)

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
            PrintToLogs(LogType.Error, "No project is selected")
        elif project_path != None:
            PrintToLogs(LogType.Log, f"Project path is: {project_path}")
            self.project_dir = project_path
        self.create_content_drawer()
        self.root.mainloop()

    def create_menubar(self):
        menubar=tk.Menu(self.root)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Open")
        file_menu.add_command(label="Save")
        menubar.add_cascade(label="File", menu=file_menu)

        edit_menu = tk.Menu(menubar, tearoff=0)
        edit_menu.add_command(label="Undo")
        edit_menu.add_command(label="Redo")
        edit_menu.add_command(label="Cut")
        edit_menu.add_command(label="Copy")
        edit_menu.add_command(label="Paste")
        edit_menu.add_separator()
        edit_menu.add_command(label="Project Settings", command=self.open_project_settings)
        edit_menu.add_command(label="Preferences", command=self.open_editor_settings)
        menubar.add_cascade(label="Edit", menu=edit_menu)

        view_menu = tk.Menu(menubar, tearoff=0)
        view_menu.add_checkbutton(label="Content Drawer", command=self.toggle_content_drawer)
        menubar.add_cascade(label="View", menu=view_menu)

        self.root.config(menu=menubar)

    def create_game_canvas(self):
        pass

    def toggle_content_drawer(self):
        if self.drawer_visable:
            self.drawer.pack_forget()
        else:
            self.drawer.pack(side=tk.LEFT, fill=tk.Y, padx=5)
            self.create_content_drawer()  # Refresh content when shown
        
        self.drawer_visable = not self.drawer_visable

    def create_content_drawer(self):
        # Clear the tree first
        for item in self.project_tree.get_children():
            self.project_tree.delete(item)
        if self.project_dir:
            content_dir = os.path.join(self.project_dir, "content")
            if os.path.isdir(content_dir):
                self.insert_tree_items(content_dir, "")
            else:
                self.project_tree.insert("", tk.END, text="No 'content' folder found.")
        else:
            self.project_tree.insert("", tk.END, text="No project loaded.")

    def insert_tree_items(self, path, parent):
        # List folders first, then files, and hide .DS_Store
        try:
            entries = sorted(
                [e for e in os.listdir(path) if e != ".DS_Store"],
                key=lambda x: (not os.path.isdir(os.path.join(path, x)), x.lower())
            )
            for entry in entries:
                full_path = os.path.join(path, entry)
                if os.path.isdir(full_path):
                    node = self.project_tree.insert(parent, tk.END, text=entry, open=False)
                    self.insert_tree_items(full_path, node)
                else:
                    self.project_tree.insert(parent, tk.END, text=entry)
        except Exception as e:
            self.project_tree.insert(parent, tk.END, text=f"Error: {e}")

    def on_tree_left_click(self, event):
        # Show context menu on left click
        item_id = self.project_tree.identify_row(event.y)
        if item_id:
            self.project_tree.selection_set(item_id)
            self.show_context_menu(event)

    def on_tree_right_click(self, event):
        # Also support right click for context menu
        item_id = self.project_tree.identify_row(event.y)
        if item_id:
            self.project_tree.selection_set(item_id)
            self.show_context_menu(event)

    def show_context_menu(self, event):
        menu = tk.Menu(self.root, tearoff=0)
        menu.add_command(label="Cut", command=self.cut_item)
        menu.add_command(label="Copy", command=self.copy_item)
        menu.add_command(label="Paste", command=self.paste_item)
        menu.add_separator()
        menu.add_command(label="Delete", command=self.delete_item)
        menu.tk_popup(event.x_root, event.y_root)

    def cut_item(self):
        # Implement cut logic here
        pass

    def copy_item(self):
        # Implement copy logic here
        pass

    def paste_item(self):
        # Implement paste logic here
        pass

    def delete_item(self):
        selected = self.project_tree.selection()
        if selected:
            path = self.get_full_path_from_tree(selected[0])
            import shutil
            try:
                if os.path.isdir(path):
                    shutil.rmtree(path)
                else:
                    os.remove(path)
                self.create_content_drawer()
            except Exception as e:
                tk.messagebox.showerror("Error", f"Could not delete: {e}")

    def add_file(self):
        import tkinter.simpledialog
        filename = tk.simpledialog.askstring("Add File", "Enter new file name:")
        if filename and self.project_dir:
            # Determine selected directory in the tree
            selected = self.project_tree.selection()
            if selected:
                # Get full path of selected node
                node = selected[0]
                parent_path = self.get_full_path_from_tree(node)
            else:
                # Default to content directory
                parent_path = os.path.join(self.project_dir, "content")
            if not os.path.isdir(parent_path):
                parent_path = os.path.dirname(parent_path)
            os.makedirs(parent_path, exist_ok=True)
            file_path = os.path.join(parent_path, filename)
            if not os.path.exists(file_path):
                with open(file_path, "w") as f:
                    f.write("")  # Create empty file
                self.create_content_drawer()
            else:
                tk.messagebox.showerror("Error", "File already exists.")

    def get_full_path_from_tree(self, node):
        # Recursively build the path from the tree node
        parts = []
        while node:
            name = self.project_tree.item(node, "text")
            parts.insert(0, name)
            node = self.project_tree.parent(node)
        # Join with content directory as root
        return os.path.join(self.project_dir, "content", *parts)

    def add_folder(self):
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

    def on_tree_double_click(self, event):
        # Get the item that was double-clicked
        item_id = self.project_tree.focus()
        if not item_id:
            return
        path = self.get_full_path_from_tree(item_id)
        if os.path.isfile(path):
            ext = os.path.splitext(path)[1].lower()
            language = self.get_language_from_extension(ext)
            self.open_code_editor(path, language)

    def get_language_from_extension(self, ext):
        # Map file extensions to language names
        ext_map = {
            '.py': 'python',
            '.js': 'javascript',
            '.json': 'json',
            '.html': 'html',
            '.css': 'css',
            '.cpp': 'cpp',
            '.c': 'c',
            '.h': 'cpp',
            '.cs': 'csharp',
            '.java': 'java',
            '.txt': 'text',
            # Add more as needed
        }
        return ext_map.get(ext, 'text')

    def open_code_editor(self, filename=None, language='text'):
        from Editor.CodeEditor import CodeEditor
        CodeEditor(filename, self.project_dir, language=language)


    def open_project_settings(self):
        ProjectSettings()

    def open_editor_settings(self):
        EditorSettingsWindow()