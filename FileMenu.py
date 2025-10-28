import tkinter as tk
import pickle
from DataStructs import LayerList
class FileMenu():
    def __init__(self,root, parent):
        
        self.parent = parent
        
        self.file_btn = tk.Menubutton(root, text="File", relief="raised")
        self.file_btn.pack(anchor=tk.NW, padx=10, pady=10)
        self.file_btn.menu = tk.Menu(self.file_btn, tearoff=0)
        self.file_btn["menu"] = self.file_btn.menu

        self.file_btn.menu.add_command(label="New Project")
        self.file_btn.menu.add_command(label="Open", command=self.load)         
        self.file_btn.menu.add_command(label="Save", command=self.save)
        self.file_btn.menu.add_command(label="Exit")
    def save(self):
        """save class as self.name.txt"""
        file = open('save.ptky','wb')
        ll = LayerList()
        ll.layers = self.parent.layers.copy()
        file.write(pickle.dumps(ll))
        file.close()

    def load(self):
        """try load self.name.txt"""
        file = open('save.ptky','rb')
        dataPickle = file.read()
        file.close()
        ll = pickle.loads(dataPickle)
        self.parent.layers = ll.layers
        self.parent.UpdateLayers()
        self.parent.UpdateDisplay()