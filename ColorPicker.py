import tkinter as tk
from PIL import Image, ImageTk
import numpy as np
class ColorPalette(tk.Frame):
    def __init__(self, root,  **kwargs):
        super().__init__(root, **kwargs)
        
        self.canvas = tk.Canvas(self, width=100, height=100)
        
        self.canvas.pack(side=tk.TOP)

        self.red = tk.Scale(self, label="red", from_=0, to=255, orient=tk.HORIZONTAL, command=self.updateCanvas)
        self.red.pack()
        self.green = tk.Scale(self, label="green" , from_=0, to=255, orient=tk.HORIZONTAL, command=self.updateCanvas)
        self.green.pack()
        self.blue = tk.Scale(self , label="blue" , from_=0, to=255, orient=tk.HORIZONTAL, command=self.updateCanvas)
        self.blue.pack()

        self.canvas_color = np.ones((100,100, 3), dtype = np.uint8 )
        img = Image.fromarray(self.canvas_color)
        self.photo_img = ImageTk.PhotoImage(image=img)
        self.image_element = self.canvas.create_image(1,1,image=self.photo_img, anchor="nw")

        self.currentColor = [self.red.get(),self.green.get(),self.blue.get()]
    def updateCanvas(self, value):
        #[1,1,1] * current color
        self.canvas_color =np.multiply( np.ones((100,100, 3) ), np.array([self.red.get(),self.green.get(),self.blue.get()]))
        img = Image.fromarray(self.canvas_color.astype(np.uint8))
        self.photo_img = ImageTk.PhotoImage(image=img)
        self.canvas.itemconfig(self.image_element, image = self.photo_img)
        self.currentColor = [self.red.get(),self.green.get(),self.blue.get()]


