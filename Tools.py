import math
import numpy as np
class Tool:
    def __init__(self, parent):
        self.parent = parent
    def getBrushArea(self, pos_x, pos_y):
        arr = []
        for i in range(pos_x - self.size, pos_x + self.size):
            for j in range(pos_y - self.size, pos_y + self.size):
                dist = math.sqrt(((pos_x - i)**2 + (pos_y - j)**2))
            
                if(dist <= self.size):
                    arr.append([i,j])
        return arr
    def getGridArea(self, pos_x, pos_y):
        arr = []
        grid_x = pos_x // self.parent.gridSize
        grid_y = pos_y // self.parent.gridSize
        return (grid_x * self.parent.gridSize, grid_y * self.parent.gridSize)
    def execute(self, event):
        pass
class Brush(Tool):
    def __init__(self, parent):
        super().__init__(parent)
    def execute(self, event):
        '''area = self.brush.getBrushArea(event.x, event.y)
        for i in range(len(area)):
            if (area[i][0] > 0 and area[i][0] < len(self.base[0])) and (area[i][1] > 0 and area[i][1] < len(self.base.data)):
                self.layers[self.currentLayerIndex].frame_pointer.content[area[i][1]][area[i][0]] = self.ColorPickerModule.currentColor
                self.layers[self.currentLayerIndex].frame_pointer.alpha[area[i][1]][area[i][0]] = 255
                self.CalculatePixel(area[i][1], area[i][0])
        '''
        grid_area = self.getGridArea(event.x, event.y)
        grid_size = self.parent.gridSize
        self.parent.layers[self.parent.currentLayerIndex].frame_pointer.content[grid_area[1]: grid_area[1] + grid_size, grid_area[0]: grid_area[0] + grid_size] = self.parent.ColorPickerModule.currentColor
        self.parent.layers[self.parent.currentLayerIndex].frame_pointer.alpha[grid_area[1]: grid_area[1] + grid_size, grid_area[0]: grid_area[0] + grid_size] = 255
        
        for i in range(grid_size):
            for  j in range(grid_size):
                
                self.parent.CalculatePixel(grid_area[1] + i, grid_area[0] + j)
        self.parent.UpdateDisplay()
        
class Eraser(Tool):
    def __init__(self, parent):
        super().__init__(parent)
    def execute(self, event):
        grid_area = self.getGridArea(event.x, event.y)
        grid_size = self.parent.gridSize
        self.parent.layers[self.parent.currentLayerIndex].frame_pointer.alpha[grid_area[1]: grid_area[1] + grid_size, grid_area[0]: grid_area[0] + grid_size] = 0
        for i in range(grid_size):
            for  j in range(grid_size):
                
                self.parent.CalculatePixel(grid_area[1] + i, grid_area[0] + j)
        self.parent.UpdateDisplay()
        
    
    
    


