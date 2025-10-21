import tkinter as tk
from tkinter import ttk
from tkinter import *
 
class Scrollable(tk.Frame):
    """
       Make a frame scrollable with scrollbar on the right.
       After adding or removing widgets to the scrollable frame, 
       call the update() method to refresh the scrollable area.
    """
 
    def __init__(self, frame, width=16):
 
        scrollbar = tk.Scrollbar(frame, width=width)
        
 
        self.canvas = tk.Canvas(frame, yscrollcommand=scrollbar.set, width= 100)
        self.canvas.pack(side=tk.LEFT,  fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.LEFT, fill=tk.Y)
        scrollbar.config(command=self.canvas.yview)
 
        #self.canvas.bind('<Configure>', self.__fill_canvas)
 
        # base class initialization
        tk.Frame.__init__(self, frame, height= 100)         
 
        # assign this obj (the inner frame) to the windows item of the canvas
        self.windows_item = self.canvas.create_window(0,0, window=self, anchor=tk.NW)
 
 
    def __fill_canvas(self, event):
        "Enlarge the windows item to the canvas width"
 
        canvas_width = event.width
        self.canvas.itemconfig(self.windows_item, width = canvas_width)        
 
    def update(self):
        "Update the canvas and the scrollregion"
 
        self.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox(self.windows_item))