import tkinter as tk
import pickle
from DataStructs import ProjectSettings
class FileMenu():
    def __init__(self,root, parent):
        
        self.parent = parent
        self.root = root
        self.file_btn = tk.Menubutton(root, text="File", relief="raised")
        self.file_btn.pack(anchor=tk.NW, padx=10, pady=10)
        self.file_btn.menu = tk.Menu(self.file_btn, tearoff=0)
        self.file_btn["menu"] = self.file_btn.menu

        self.file_btn.menu.add_command(label="New Project", command=self.new_project)
        self.file_btn.menu.add_command(label="Open", command=self.open_file)         
        self.file_btn.menu.add_command(label="Save", command=self.save)
        self.file_btn.menu.add_command(label="Exit", command=self.on_close)

        self.name_variable = tk.StringVar()
        self.width_variable = tk.IntVar()
        self.height_variable = tk.IntVar()
    def new_project(self):
        self.new_project_window = tk.Toplevel(self.root)
        self.new_project_window.title("New Project")
        self.new_project_window.geometry("300x200")
        np_grid = tk.Frame(self.new_project_window)
        
        
        
        name_label = tk.Label(np_grid, text="project name")
        name_label.grid(column=0, row=0)
        project_name_entry = tk.Entry(np_grid, width=30, textvariable=self.name_variable)
        project_name_entry.grid(column=1, row = 0)

        width_label = tk.Label(np_grid, text="width")
        width_label.grid(column=0, row=1)
        width_input = tk.Spinbox(np_grid, from_ = 1, to = 10000, width=30, textvariable=self.width_variable)
        width_input.grid(column=1, row = 1)

        height_label = tk.Label(np_grid, text="height")
        height_label.grid(column=0, row=2)
        height_input = tk.Spinbox(np_grid, from_ = 1, to = 10000, width=30, textvariable=self.height_variable)
        height_input.grid(column=1, row = 2)


        np_grid.pack()

        create_button = tk.Button(self.new_project_window, text="create", command=self.create_new_project)
        create_button.pack()

        close_button = tk.Button(self.new_project_window, text="Close", command=self.new_project_window.destroy)
        close_button.pack()
    def create_new_project(self):
        print(self.name_variable.get())
        print(self.height_variable.get())
        print(self.width_variable.get())
        new_project_settings = ProjectSettings(_name = self.name_variable.get(), width= self.width_variable.get(), height=self.height_variable.get())
        self.parent.reset_program(new_project_settings)
        self.new_project_window.destroy()
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
            #ll = ProjectSettings()
            #ll.layers = self.parent.layers.copy()
            #file.write(pickle.dumps(ll))
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