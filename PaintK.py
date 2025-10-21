from tkinter import *

from PIL import Image, ImageTk
import numpy as np

import Tools
from Layer import Layer
import customtkinter as ctk
from FileMenu import FileMenu
from ColorPicker import ColorPalette
class MainWindow:
    def __init__(self, root, width, height):

        self.width = width
        self.height = height
        root.title("PaintK")
        # Set geometry (widthxheight)
        root.geometry('1000x500')
        self.canvas = Canvas(root, bg="green", height=self.height, width=self.width)

        self.brush = Tools.Brush()
        self.layers = []
        self.currentLayerIndex = 0
        self.base = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        grid = 10
        for i in range(0,self.height, grid):
            end_i = i+grid
            
            #if end_i >= self.height: 
            #    end_i = self.height -1
            for j in range(0,self.width, grid):
                end_j = j+grid
                #if end_j >= self.width: 
                #    end_j = self.width -1
                    
                #print("values:{i} + {j} = {self.a}" )
                if ((i + j)//10)%2==0:
                    #print("red " + str(i) + " and " + str(j))
                    self.base[i: end_i,j: end_j] = [255,255,255]
                else:
                    #print("black " + str(i) + " and " + str(j))
                    self.base[i: end_i,j: end_j] = [100,100,100]
            
       
        self.display = self.base



        img = Image.fromarray(self.base)
        self.photo_img = ImageTk.PhotoImage(image=img)
        self.image_element = self.canvas.create_image(1,1,image=self.photo_img, anchor="nw")
        
        self.canvas.bind("<B1-Motion>", self.paint)
        self.FileMenuModule = FileMenu(root)
        self.addColorPickerModule(root)
        self.canvas.pack(side=LEFT)

        self.addLayerModule(root)
        
    def AddLayer(self):
        newLayer = Layer(self.width, self.height, 50)
        
        Button(self.layerList, text = "Layer"+ str(newLayer.id), width= 20, command=lambda idx = newLayer.id: self.setLayer(idx)  ).grid(column=0,row= 200 - len(self.layers))
        Button(self.layerList, text = "B", width= 5, command=lambda idx = newLayer.id: self.toggleLayerVisibility(idx)).grid(column=1,row=200 - len(self.layers))
        self.layers.append(newLayer)
        self.UpdateLayers()
        self.UpdateDisplay()
    def setLayer(self, index):
        
        for i in range(len(self.layers)):
            if(self.layers[i].id == index):
                print("picked " + str(i))
                self.currentLayerIndex = i
                break
    def toggleLayerVisibility(self, index):
        print("toggling: " + str(index))
        for i in range(len(self.layers)):
            if(self.layers[i].id == index):
                self.layers[i].visible = not self.layers[i].visible 
                break
        self.UpdateLayers()
        self.UpdateDisplay()
    def UpdateLayers(self):
        self.display = self.base
        for i in range(len(self.layers)):
            self.display = self.layers[i].normal(self.display)
    def UpdateDisplay(self):
        img = Image.fromarray(self.display)
        self.photo_img = ImageTk.PhotoImage(image=img)
        self.canvas.itemconfig(self.image_element, image = self.photo_img)
    def CalculatePixel(self, x, y):
        ret = self.base[x][y]
        for i in range(len(self.layers)):
            ret = self.layers[i].normal_pixel(ret, x, y)
        self.display[x][y] = ret


    def addLayerModule(self, root):
        self.layerModule = Frame(root, bg="lightblue", padx=10, pady=10, height= 300)
        self.layerList = ctk.CTkScrollableFrame(self.layerModule, width = 200, height= 30)
        self.AddLayerBtn = Button(self.layerModule, text="+", width= 3, height=3, command=self.AddLayer)
        
        self.layerModule.pack(side=LEFT)
        self.layerList.pack(side=TOP)
        Frame(self.layerModule, bg="red", height=50).pack(side=TOP)
        self.AddLayerBtn.place(relx=1.0, rely=1.0, anchor="se")

    def addColorPickerModule(self, root):
        
        
        self.ColorPickerModule = ColorPalette(root, bg="lightblue", padx=10, pady=10,width=200, height= 300)
        self.ColorPickerModule.pack(side=LEFT)
    def paint(self, event):
        if len(self.layers) == 0: return
        area = self.brush.getBrushArea(event.x, event.y)
        for i in range(len(area)):
            if (area[i][0] > 0 and area[i][0] < len(self.base[0])) and (area[i][1] > 0 and area[i][1] < len(self.base.data)):
                self.layers[self.currentLayerIndex].content[area[i][1]][area[i][0]] = self.ColorPickerModule.currentColor
                self.layers[self.currentLayerIndex].alpha[area[i][1]][area[i][0]] = 255
                self.CalculatePixel(area[i][1], area[i][0])
        self.UpdateDisplay()


root = Tk()

window = MainWindow(root, 500, 250)


root.mainloop()