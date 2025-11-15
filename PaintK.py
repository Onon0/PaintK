from tkinter import *

from PIL import Image, ImageTk
import numpy as np

import Tools
from DataStructs import Layer
from FileMenu import FileMenu
from Modules import ColorPalette, AnimationModule, LayerModule, ToolsModule

class MainWindow:
    def __init__(self, root, width, height):

        self.width = width
        self.height = height
        self.root = root
        
        root.title("untitled")
        # Set geometry (widthxheight)
        root.geometry('1000x600')

        self.MiddleContainer = Frame(root)
        self.BottomContainer = Frame(root)

        self.tool = Tools.Brush(self)
        self.layers = []
        self.currentLayerIndex = 0
        self.currentFrameIndex = 0

        ''' grid variables '''
        self.grid = Layer(self.width, self.height)
        self.gridSize = 10
        self.bShowGrid = BooleanVar(value=False)
        self.showGrid()
        
        
        

        
        self.FileMenuModule = FileMenu(root, self)
        
        self.addToolsModule(root)
        self.addColorPickerModule(self.MiddleContainer)
        
        
        self.addCanvasModule()

        self.addLayerModule(self.MiddleContainer)
        self.addAnimationModule(self.BottomContainer)
        self.MiddleContainer.pack(side=TOP)
        self.BottomContainer.pack(side=TOP)
        
    
    def UpdateLayers(self):
        self.display = self.base
        
        for i in range(len(self.layers)):
            self.layers[i].find_frame(self.currentFrameIndex)
        #---------onion skinning------------#
        for i in range(len(self.layers)):
            onion = self.layers[i].get_onion()
            if onion != None:
                self.display = onion.normal(self.display)
        #---------onion skinning------------#

        for i in range(len(self.layers)):
            self.display = self.layers[i].frame_pointer.normal(self.display)
        if self.bShowGrid.get():
            self.display = self.grid.normal(self.display)
    def UpdateDisplay(self):
        img = Image.fromarray(self.display)
        self.photo_img = ImageTk.PhotoImage(image=img)
        self.canvas.itemconfig(self.image_element, image = self.photo_img)
    def CalculatePixel(self, x, y):
        if x <= 0 or x >= self.height:
            return
        if y <=0 or y >= self.width:
            return 
        ret = self.base[x][y]
        for i in range(len(self.layers)):
            ret = self.layers[i].normal_pixel(ret, x, y)
        
        if self.bShowGrid.get():
            ret = self.grid.normal_pixel(ret,x,y)
        self.display[x][y] = ret
        
    def showGrid(self):
        
        for i in range(0, self.height, self.gridSize):
            self.grid.frame_pointer.content[i][:] = [255,0,0]
            self.grid.frame_pointer.alpha[i][:] = 255
        
        for i in range(0, self.width, self.gridSize):
            self.grid.frame_pointer.content[:,i] = [255,0,0]
            self.grid.frame_pointer.alpha[:,i] = 255

    def toggleGrid(self):
        self.UpdateLayers()
        self.UpdateDisplay()
    def addCanvasModule(self):
        self.canvasModule = Frame(self.MiddleContainer, width=self.width)
        self.canvas = Canvas(self.canvasModule, height=self.height, width=self.width)
        self.gridToggle = Checkbutton(self.canvasModule, text = "show grid", variable=self.bShowGrid, onvalue=True, offvalue=False, command=self.toggleGrid)
        self.create_base()
        img = Image.fromarray(self.base)
        self.photo_img = ImageTk.PhotoImage(image=img)
        self.image_element = self.canvas.create_image(1,1,image=self.photo_img, anchor="nw")
        
        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind("<Button-1>", self.mouse_drag_start)
        self.canvas.bind("<ButtonRelease-1>", self.mouse_drag_end)
        self.canvas.pack(side=TOP)
        self.gridToggle.pack(side=TOP)
        self.canvasModule.pack(side=LEFT)

    def create_base(self):
        self.base = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        '''draw transparent layer grid '''
        base_grid = 10
        for i in range(0,self.height, base_grid):
            end_i = i+base_grid
            
            if end_i >= self.height: 
                end_i = self.height -1
            for j in range(0,self.width, base_grid):
                end_j = j+base_grid
                if end_j >= self.width: 
                    end_j = self.width -1
                    
                
                if ((i + j)//10)%2==0:
                    self.base[i: end_i,j: end_j] = [255,255,255]
                else:
                    self.base[i: end_i,j: end_j] = [100,100,100]
        '''draw transparent layer grid '''
       
        self.display = self.base
        

    def addLayerModule(self, root):
        self.layerModule = LayerModule(root, self)
        self.layerModule.pack(side=LEFT)

    def addColorPickerModule(self, root):
        
        
        self.ColorPickerModule = ColorPalette(root, bg="lightblue", padx=10, pady=10,width=200, height= 300)
        self.ColorPickerModule.pack(side=LEFT)
    def addAnimationModule(self, root):
        self.AnimationModule = AnimationModule(root, self,width= 1000)
        self.AnimationModule.pack(side=LEFT)
    
    def addToolsModule(self, root):
        self.ToolsModule = ToolsModule(root, self, width = 15, height = 5)
        self.ToolsModule.pack(side=TOP)
    def reset_program(self, new_settings):
        self.width = new_settings.width
        self.height = new_settings.height
        self.root.title(new_settings.project_name)
        self.canvas.configure(width=self.width, height=self.height)
        self.grid = Layer(self.width, self.height)
        self.layers = new_settings.layers
        self.create_base()
        self.UpdateLayers()
        self.UpdateDisplay()
        self.layerModule.refreshLayerItems()
        
    def setPixel(self, x, y):
        self.layers[self.currentLayerIndex].frame_pointer.content[y][x] = self.ColorPickerModule.currentColor
        self.layers[self.currentLayerIndex].frame_pointer.alpha[y][x] = 255
        self.CalculatePixel(y,x)
    def setGridPixel(self, x, y):
        grid_x = x // self.gridSize
        grid_y = y // self.gridSize
        grid_area = (grid_x * self.gridSize, grid_y * self.gridSize)

        self.layers[self.currentLayerIndex].frame_pointer.content[grid_area[1]: grid_area[1] + self.gridSize, grid_area[0]: grid_area[0] + self.gridSize] = self.ColorPickerModule.currentColor
        self.layers[self.currentLayerIndex].frame_pointer.alpha[grid_area[1]: grid_area[1] + self.gridSize, grid_area[0]: grid_area[0] + self.gridSize] = 255
        for i in range(self.gridSize):
            for  j in range(self.gridSize):
                
                self.CalculatePixel(grid_area[1] + i, grid_area[0] + j)
    def paint(self, event):
        if len(self.layers) == 0: return
        if not self.layers[self.currentLayerIndex].frame_exist(self.currentFrameIndex):
            
            self.layers[self.currentLayerIndex].add_frame_at(self.currentFrameIndex)
            self.layers[self.currentLayerIndex].print_frame()
            self.UpdateLayers()
            self.UpdateDisplay()
        
        self.tool.execute(event=event)
    
    def mouse_drag_start(self, event):
        if len(self.layers) == 0: return
        if not self.layers[self.currentLayerIndex].frame_exist(self.currentFrameIndex):
            
            self.layers[self.currentLayerIndex].add_frame_at(self.currentFrameIndex)
            self.layers[self.currentLayerIndex].print_frame()
            self.UpdateLayers()
            self.UpdateDisplay()
        
        self.tool.drag_start(event=event)
    
    def mouse_drag_end(self, event):
        if len(self.layers) == 0: return
        if not self.layers[self.currentLayerIndex].frame_exist(self.currentFrameIndex):
            
            self.layers[self.currentLayerIndex].add_frame_at(self.currentFrameIndex)
            self.layers[self.currentLayerIndex].print_frame()
            self.UpdateLayers()
            self.UpdateDisplay()
        
        self.tool.drag_end(event=event)



root = Tk()

window = MainWindow(root, 500, 250)


root.mainloop()