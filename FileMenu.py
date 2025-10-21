import tkinter as tk
class FileMenu():
    def __init__(self,root):
        
        
        self.file_btn = tk.Menubutton(root, text="File", relief="raised")
        self.file_btn.pack(anchor=tk.NW, padx=10, pady=10)
        self.file_btn.menu = tk.Menu(self.file_btn, tearoff=0)
        self.file_btn["menu"] = self.file_btn.menu

        self.file_btn.menu.add_command(label="New Project")
        self.file_btn.menu.add_command(label="Open")         
        self.file_btn.menu.add_command(label="Save")
        self.file_btn.menu.add_command(label="Exit")
