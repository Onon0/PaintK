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
        self.file_btn.menu.add_command(label="Open", command=self.open_file)         
        self.file_btn.menu.add_command(label="Save", command=self.save)
        self.file_btn.menu.add_command(label="Exit", command=self.on_close)
    def save(self):
        filepath = tk.filedialog.asksaveasfilename(
            title="Select a file",
            initialdir="/",  # Start in the root directory
            defaultextension=".ptky",
            filetypes=[("paintk file", "*.ptky")]
        )
        if filepath:
            print(filepath)
            file = open(filepath,'wb')
            ll = LayerList()
            ll.layers = self.parent.layers.copy()
            file.write(pickle.dumps(ll))
            file.close()

    
    def open_file(self):
        filepath = tk.filedialog.askopenfilename(
            title="Select a file",
            initialdir="/",  # Start in the root directory
            filetypes=[("Text files", "*.ptky"), ("All files", "*.*")]
        )
        if filepath:
            file = open(filepath,'rb')
            dataPickle = file.read()
            file.close()
            ll = pickle.loads(dataPickle)
            self.parent.layers = ll.layers
            self.parent.UpdateLayers()
            self.parent.UpdateDisplay()
            self.parent.layerModule.refreshLayerItems()
    def on_close(self):
        if tk.messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.parent.root.destroy()