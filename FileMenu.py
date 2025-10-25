import tkinter as tk
import pickle
class FileMenu():
    def __init__(self,root, parent):
        
        self.parent = parent
        
        self.file_btn = tk.Menubutton(root, text="File", relief="raised")
        self.file_btn.pack(anchor=tk.NW, padx=10, pady=10)
        self.file_btn.menu = tk.Menu(self.file_btn, tearoff=0)
        self.file_btn["menu"] = self.file_btn.menu

        self.file_btn.menu.add_command(label="New Project")
        self.file_btn.menu.add_command(label="Open")         
        self.file_btn.menu.add_command(label="Save", command=self.save)
        self.file_btn.menu.add_command(label="Exit")
    def save(self):
        with open(f'save.ptky', 'wb') as file:
            pickle.dump(self.parent, file)