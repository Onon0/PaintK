from tkinter import *

from PIL import Image, ImageTk
import numpy as np

import Tools
from DataStructs import Layer
from FileMenu import FileMenu
from Modules import ColorPalette, AnimationModule, LayerModule

class MainWindow:
    def __init__(self, root, width, height):

        self.width = width
        self.height = height
        root.title("PaintK")
        # Set geometry (widthxheight)
        root.geometry('1000x500')

        self.MiddleContainer = Frame(root)
        self.BottomContainer = Frame(root)
        self.canvas = Canvas(self.MiddleContainer, bg="green", height=self.height, width=self.width)

        self.brush = Tools.Brush()
        self.layers = []
        self.grid = Layer(self.width, self.height)
        self.showGrid()
        self.currentLayerIndex = 0
        self.currentFrameIndex = 0
        
        self.base = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        #draw transparent layer grid
        grid = 10
        for i in range(0,self.height, grid):
            end_i = i+grid
            
            if end_i >= self.height: 
                end_i = self.height -1
            for j in range(0,self.width, grid):
                end_j = j+grid
                if end_j >= self.width: 
                    end_j = self.width -1
                    
                
                if ((i + j)//10)%2==0:
                    self.base[i: end_i,j: end_j] = [255,255,255]
                else:
                    self.base[i: end_i,j: end_j] = [100,100,100]
            
       
        self.display = self.base

        

        img = Image.fromarray(self.base)
        self.photo_img = ImageTk.PhotoImage(image=img)
        self.image_element = self.canvas.create_image(1,1,image=self.photo_img, anchor="nw")
        
        self.canvas.bind("<B1-Motion>", self.paint)
        self.FileMenuModule = FileMenu(root, self)
        
        self.addColorPickerModule(self.MiddleContainer)
        
        self.canvas.pack(side=LEFT)

        self.addLayerModule(self.MiddleContainer)
        self.addAnimationModule(self.BottomContainer)
        self.MiddleContainer.pack(side=TOP)
        self.BottomContainer.pack(side=TOP)
        
    
    def UpdateLayers(self):
        self.display = self.base
        for i in range(len(self.layers)):
            self.display = self.layers[i].find_frame(self.currentFrameIndex).normal(self.display)
        self.display = self.grid.normal(self.display)
    def UpdateDisplay(self):
        img = Image.fromarray(self.display)
        self.photo_img = ImageTk.PhotoImage(image=img)
        self.canvas.itemconfig(self.image_element, image = self.photo_img)
    def CalculatePixel(self, x, y):
        ret = self.base[x][y]
        for i in range(len(self.layers)):
            ret = self.layers[i].normal_pixel(ret, x, y)
        
        ret = self.grid.normal_pixel(ret,x,y)
        self.display[x][y] = ret
        
    def showGrid(self):
        grid = 50
    
        for i in range(0, self.height, grid):
            self.grid.frame_pointer.content[i][:] = [255,0,0]
            self.grid.frame_pointer.alpha[i][:] = 255
        
        for i in range(0, self.width, grid):
            self.grid.frame_pointer.content[:,i] = [255,0,0]
            self.grid.frame_pointer.alpha[:,i] = 255

        print(self.grid.frame_pointer.content.shape)

    def addLayerModule(self, root):
        self.layerModule = LayerModule(root, self)
        self.layerModule.pack(side=LEFT)

    def addColorPickerModule(self, root):
        
        
        self.ColorPickerModule = ColorPalette(root, bg="lightblue", padx=10, pady=10,width=200, height= 300)
        self.ColorPickerModule.pack(side=LEFT)
    def addAnimationModule(self, root):
        self.AnimationModule = AnimationModule(root, self,width= 1000)
        self.AnimationModule.pack(side=LEFT)
    def paint(self, event):
        if len(self.layers) == 0: return
        if not self.layers[self.currentLayerIndex].frame_exist(self.currentFrameIndex):
            
            self.layers[self.currentLayerIndex].add_frame_at(self.currentFrameIndex)
            self.layers[self.currentLayerIndex].print_frame()
            self.UpdateLayers()
            self.UpdateDisplay()
        area = self.brush.getBrushArea(event.x, event.y)
        for i in range(len(area)):
            if (area[i][0] > 0 and area[i][0] < len(self.base[0])) and (area[i][1] > 0 and area[i][1] < len(self.base.data)):
                self.layers[self.currentLayerIndex].frame_pointer.content[area[i][1]][area[i][0]] = self.ColorPickerModule.currentColor
                self.layers[self.currentLayerIndex].frame_pointer.alpha[area[i][1]][area[i][0]] = 255
                self.CalculatePixel(area[i][1], area[i][0])
        self.UpdateDisplay()


root = Tk()

window = MainWindow(root, 500, 250)


root.mainloop()