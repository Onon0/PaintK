import math
import numpy as np
class Brush:
    def __init__(self, parent):
        self.parent = parent
        self.size = 10
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

