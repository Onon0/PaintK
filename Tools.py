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

    def execute(self, event):
        pass
    def drag_start(self, event):
        pass
    def drag_end(self, event):
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
        
        self.parent.setGridPixel(event.x, event.y)
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
        
class Line(Tool):
    def __init__(self, parent):
        super().__init__(parent)
        self.line_start = np.array([0,0])
        self.line_end = np.array([0,0])
    def execute(self, event):
        pass
    def drag_start(self, event):
        print(f"start at {event.x} , {event.y}")
        self.line_start[0] = event.x
        self.line_start[1] = event.y
    def drag_end(self, event):
        print(f"end at {event.x} , {event.y}")
        self.line_end[0] = event.x
        self.line_end[1] = event.y

        line = self.line_end - self.line_start
        magnitude = int(np.linalg.norm(line))
        perp_1 = np.array([-line[1], line[0]])/ magnitude
        perp_2 = np.array([line[1], -line[0]])/ magnitude
        print(magnitude)
        for i in range(0, magnitude):
            inc = i / (magnitude)
            point = self.line_start * (1 - inc) + self.line_end * inc
            point = point.astype(np.uint64)
            self.parent.setGridPixel(point[0], point[1])
            


        '''
        x_start = min(self.line_start[0] , self.line_end[0])
        y_start = min(self.line_start[1] , self.line_end[1])

        x_end = max(self.line_start[0] , self.line_end[0])
        y_end = max(self.line_start[1] , self.line_end[1])
        
        line = self.line_end - self.line_start
        for i in range(x_start, x_end):
            for j in range(y_start, y_end):
                vec = np.array([i,j]) - self.line_start
                #cross = line[0]*vec[1] - line[1]*vec[0]
                cross = np.cross(line, vec)
                magnitude = np.linalg.norm(line)
                #print(cross)
                if abs(cross)/magnitude < 10:
                    self.parent.layers[self.parent.currentLayerIndex].frame_pointer.content[j][i] = self.parent.ColorPickerModule.currentColor
                    self.parent.layers[self.parent.currentLayerIndex].frame_pointer.alpha[j][i] = 255
                    self.parent.CalculatePixel(j, i)
        '''
        self.parent.UpdateDisplay()
        
        

        
    
    


