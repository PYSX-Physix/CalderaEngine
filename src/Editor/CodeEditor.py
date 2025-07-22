import tkinter as tk
from tkinter import scrolledtext
import os
import keyword
import re
import importlib
import importlib.metadata
import inspect

class CodeEditor(tk.Toplevel):
    def __init__(self, filename, project_dir, language='text'):
        super().__init__()
        self.title(f"Code Editor - {os.path.basename(filename)}")
        self.editor_root = tk.Frame(self)
        self.editor_root.pack(fill=tk.BOTH, expand=True)
        self.geometry("800x600")
        self.filename = filename
        self.language = language
        self.project_dir= project_dir
        self.text = scrolledtext.ScrolledText(self.editor_root, wrap=tk.NONE, undo=True)
        self.text.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
        self.import_list_frame = tk.Frame(self.editor_root, width=200)
        self.import_list_frame.pack(side=tk.RIGHT, fill=tk.Y)
        self.create_import_list()  # Initialize with an empty list

        self.text.bind('<KeyRelease>', self.on_key_release)
        self.bind('<Control-s>', self.save_file)
        # Replace Tab with 4 spaces for Python
        if self.language == 'python':
            self.text.bind('<Tab>', self.insert_spaces)
            self.text.bind('<Shift-Tab>', self.remove_spaces)

        self.load_file()
        self.apply_syntax_highlighting()

    def create_import_list(self):
            self.import_title = tk.Label(self.import_list_frame, text="Imports", font=("Arial", 14))
            self.import_title.pack(side=tk.TOP, fill=tk.X)

            # Use importlib.metadata to get installed packages
            installed_packages = sorted([dist.metadata['Name'] for dist in importlib.metadata.distributions() if 'Name' in dist.metadata])

            # Use this to find local modules
            def find_local_modules(base_dir, prefix=""):
                modules = []
                for root, dirs, files in os.walk(base_dir):
                    rel_path = os.path.relpath(root, base_dir)
                    if rel_path == ".":
                        rel_path = ""
                    package_prefix = prefix + ("." if prefix and rel_path else "") + rel_path.replace(os.sep, ".") if rel_path != "" else prefix
                    # Add __init__.py as package
                    if "__init__.py" in files and package_prefix:
                        modules.append(package_prefix)
                        # Add .py files as modules
                    for file in files:
                        if file.endswith(".py") and file != "__init__.py":
                            mod_name = file[:-3]
                            full_mod = package_prefix + ("." if package_prefix else "") + mod_name
                            modules.append(full_mod)
                return modules

            local_modules = find_local_modules(self.project_dir)
            all_modules = sorted(set(installed_packages + local_modules))

            # --- Import form ---
            import_form = tk.Frame(self.import_list_frame)
            import_form.pack(side=tk.TOP, fill=tk.X, pady=(5, 0))

            self.import_var = tk.StringVar(import_form)
            self.import_var.set("Select module")
            self.import_menu = tk.OptionMenu(import_form, self.import_var, *all_modules, command=self.update_from_import_menu)
            self.import_menu.pack(side=tk.LEFT, fill=tk.X, expand=True)

            # --- From-import form ---
            from_import_form = tk.Frame(self.import_list_frame)
            from_import_form.pack(side=tk.TOP, fill=tk.X, pady=(5, 10))

            self.from_import_var = tk.StringVar(from_import_form)
            self.from_import_var.set("Select class/function")
            self.from_import_menu = tk.OptionMenu(from_import_form, self.from_import_var, "")
            self.from_import_menu.pack(side=tk.LEFT, fill=tk.X, expand=True)

            # Single confirm button for both
            self.confirm_import_btn = tk.Button(self.import_list_frame, text="Confirm", command=self.confirm_import_action)
            self.confirm_import_btn.pack(side=tk.TOP, padx=5, pady=(5, 0))

    def update_from_import_menu(self, selected_module):
        import inspect
        import importlib.metadata

        members = []
        tried_modules = []
        # Try to import the selected module directly
        try:
            mod = importlib.import_module(selected_module)
            tried_modules.append(selected_module)
            members = [name for name, obj in inspect.getmembers(mod) if inspect.isclass(obj) or inspect.isfunction(obj)]
        except Exception:
            # Try to get top-level modules from the distribution
            try:
                dist = importlib.metadata.distribution(selected_module)
                top_level = dist.read_text('top_level.txt')
                if top_level:
                    for top_mod in top_level.splitlines():
                        try:
                            mod = importlib.import_module(top_mod)
                            tried_modules.append(top_mod)
                            members = [name for name, obj in inspect.getmembers(mod) if inspect.isclass(obj) or inspect.isfunction(obj)]
                            if members:
                                break
                        except Exception:
                            continue
            except Exception:
                pass

        if not members:
            members = ["<Failed to import>"]
            tk.messagebox.showinfo(
                "Import Error",
                f"Could not import '{selected_module}'.\n"
                f"Tried: {', '.join(tried_modules) or selected_module}\n"
                "You may need to enter the correct module name manually."
            )

        # Update the OptionMenu
        menu = self.from_import_menu["menu"]
        menu.delete(0, "end")
        for member in members:
            menu.add_command(label=member, command=lambda value=member: self.from_import_var.set(value))
        self.from_import_var.set("Select class/function")

    def confirm_import_action(self):
        module = self.import_var.get()
        member = self.from_import_var.get()
        if (
            module
            and module != "Select module"
            and (not member or member == "Select class/function")
        ):
            # Only module selected: import statement
            self.text.insert("1.0", f"import {module}\n")
        elif (
            module
            and member
            and module != "Select module"
            and member != "Select class/function"
            and not member.startswith("<")
        ):
            # Both module and member selected: from-import statement
            self.text.insert("1.0", f"from {module} import {member}\n")

    def add_from_import_statement(self):
        module = self.import_var.get()
        member = self.from_import_var.get()
        if (
            module
            and member
            and module != "Select module"
            and member != "Select class/function"
            and not member.startswith("<")
        ):
            self.text.insert("1.0", f"from {module} import {member}\n")

    def on_import_double_click(self, event):
        selected_item = self.import_tree.selection()
        if selected_item:
            import_name = self.import_tree.item(selected_item, 'values')[0]
            # Here you can implement the logic to open the file or navigate to the import
            print(f"Double clicked on import: {import_name}")
        return "break"

    def insert_spaces(self, event):
        # Insert 4 spaces at the cursor position
        self.text.insert(tk.INSERT, "    ")
        return "break"

    def remove_spaces(self, event):
        # Remove 4 spaces before the cursor if present
        index = self.text.index(tk.INSERT)
        line_start = self.text.index(f"{index} linestart")
        current_text = self.text.get(line_start, index)
        if current_text.endswith("    "):
            self.text.delete(f"{index} -4c", index)
        return "break"

    def load_file(self):
        try:
            with open(self.filename, 'r') as f:
                content = f.read()
            self.text.delete(1.0, tk.END)
            self.text.insert(tk.END, content)
        except Exception as e:
            self.text.insert(tk.END, f"Error loading file: {e}")

    def save_file(self, event=None):
        try:
            with open(self.filename, 'w') as f:
                f.write(self.text.get(1.0, tk.END))
        except Exception as e:
            tk.messagebox.showerror("Error", f"Could not save file: {e}")

    def on_key_release(self, event=None):
        self.apply_syntax_highlighting()

    def apply_syntax_highlighting(self):
        # Remove previous tags
        self.text.tag_remove('keyword', '1.0', tk.END)
        self.text.tag_remove('string', '1.0', tk.END)
        self.text.tag_remove('comment', '1.0', tk.END)

        if self.language == 'python':
            content = self.text.get('1.0', tk.END)
            # Configure tags (do this every time to ensure they're set)
            self.text.bind('<Tab>', self.insert_spaces)
            self.text.bind('<Shift-Tab>', self.remove_spaces)
            self.text.bind('<Return>', self.auto_indent)
            self.text.tag_configure('keyword', foreground='blue')
            self.text.tag_configure('string', foreground='orange')
            self.text.tag_configure('comment', foreground='green')

            # Highlight keywords (word boundaries, multiline)
            for kw in keyword.kwlist:
                for match in re.finditer(r'\b' + re.escape(kw) + r'\b', content):
                    start = f"1.0+{match.start()}c"
                    end = f"1.0+{match.end()}c"
                    self.text.tag_add('keyword', start, end)

            # Highlight strings (single and double quotes, multiline)
            for match in re.finditer(r'(\'\'\'[\s\S]*?\'\'\'|\"\"\"[\s\S]*?\"\"\"|\'[^\']*\'|\"[^\"]*\")', content):
                start = f"1.0+{match.start()}c"
                end = f"1.0+{match.end()}c"
                self.text.tag_add('string', start, end)

            # Highlight comments (from # to end of line)
            for match in re.finditer(r'#.*', content):
                start = f"1.0+{match.start()}c"
                end = f"1.0+{match.end()}c"
                self.text.tag_add('comment', start, end)

    def auto_indent(self, event):
        # Get the current line's indentation
        line_start = self.text.index("insert linestart")
        line_end = self.text.index("insert lineend")
        line_text = self.text.get(line_start, line_end)
        indent = re.match(r'^[ \t]*', line_text).group(0)

        # Check if previous line ends with a colon (for Python blocks)
        extra_indent = ""
        if line_text.rstrip().endswith(":"):
            extra_indent = "    "  # 4 spaces

        self.text.insert("insert", f"\n{indent}{extra_indent}")
        return "break"