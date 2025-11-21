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
        self.parent.eraseGridPixel(event.x, event.y)
        self.parent.UpdateDisplay()
        
class Line(Tool):
    def __init__(self, parent):
        super().__init__(parent)
        self.line_start = np.array([0,0])
        self.line_end = np.array([0,0])
        
    def execute(self, event):
        
        self.draw_line(event)
        self.parent.UpdateLayers()
        self.parent.UpdateDisplay()
        self.parent.nullifyPreview()
        
        
    def drag_start(self, event):
        self.parent.show_preview = True
        #print(f"start at {event.x} , {event.y}")
        self.line_start[0] = event.x
        self.line_start[1] = event.y
    def drag_end(self, event):
        self.parent.show_preview = False
        self.parent.nullifyPreview()
        #print(f"end at {event.x} , {event.y}")
        self.draw_line(event)
            
        self.parent.UpdateDisplay()

    def draw_line(self, event):
        self.line_end[0] = event.x
        self.line_end[1] = event.y

        line = self.line_end - self.line_start
        magnitude = int(np.linalg.norm(line))
        perp_1 = np.array([-line[1], line[0]])/ magnitude
        perp_2 = np.array([line[1], -line[0]])/ magnitude
        for i in range(0, magnitude):
            inc = i / (magnitude)
            point = self.line_start * (1 - inc) + self.line_end * inc
            point = point.astype(np.uint64)
            self.parent.setGridPixel(point[0], point[1])
        
        
class Box(Tool):
    def __init__(self, parent):
        super().__init__(parent)
        self.line_start = np.array([0,0])
        self.line_end = np.array([0,0])
        self.preview_end = np.array([0,0])
    def execute(self, event):
        
        self.preview_end[0] = event.x
        self.preview_end[1] = event.y
        
        y_start = min(self.line_start[0] , self.preview_end[0])
        x_start = min(self.line_start[1] , self.preview_end[1])

        y_end = max(self.line_start[0] , self.preview_end[0])
        x_end = max(self.line_start[1] , self.preview_end[1])
        
        self.parent.preview.frame_pointer.content[x_start: x_end, y_start: y_end ] = self.parent.ColorPickerModule.currentColor
        self.parent.preview.frame_pointer.alpha[x_start: x_end, y_start: y_end ] = self.parent.ColorPickerModule.opacity_value
        #self.parent.CalculateArea((x_start, y_start), (x_end, y_end))
        
        
        self.parent.UpdateLayers()
        self.parent.UpdateDisplay()
        self.parent.nullifyPreview()
        
        
    def drag_start(self, event):
        self.parent.show_preview = True
        #print(f"start at {event.x} , {event.y}")
        self.line_start[0] = event.x
        self.line_start[1] = event.y
    def drag_end(self, event):
        self.parent.show_preview = False
        self.parent.nullifyPreview()
        #print(f"end at {event.x} , {event.y}")
        self.line_end[0] = event.x
        self.line_end[1] = event.y

        y_start = min(self.line_start[0] , self.line_end[0])
        x_start = min(self.line_start[1] , self.line_end[1])

        y_end = max(self.line_start[0] , self.line_end[0])
        x_end = max(self.line_start[1] , self.line_end[1])
        
        self.parent.layers[self.parent.currentLayerIndex].frame_pointer.content[x_start: x_end, y_start: y_end ] = self.parent.ColorPickerModule.currentColor
        self.parent.layers[self.parent.currentLayerIndex].frame_pointer.alpha[x_start: x_end, y_start: y_end ] = self.parent.ColorPickerModule.opacity_value
        self.parent.CalculateArea((x_start, y_start), (x_end, y_end))
        
        self.parent.UpdateDisplay()
        
class Circle(Tool):
    def __init__(self, parent):
        super().__init__(parent)
        self.line_start = np.array([0,0])
        self.line_end = np.array([0,0])
        self.preview_end = np.array([0,0])
    def execute(self, event):
        
        self.draw_circle(event)
        
        
        
        self.parent.UpdateLayers()
        self.parent.UpdateDisplay()
        self.parent.nullifyPreview()
        
        
    def drag_start(self, event):
        self.parent.show_preview = True
        #print(f"start at {event.x} , {event.y}")
        self.line_start[0] = event.x
        self.line_start[1] = event.y
    def drag_end(self, event):
        self.parent.show_preview = False
        self.parent.nullifyPreview()
        
        self.draw_circle(event)
       
        
        self.parent.UpdateDisplay()

    def draw_circle(self, event):
        self.line_end[0] = event.x
        self.line_end[1] = event.y

        w = abs(self.line_start[1] - self.line_end[1])
        h = abs(self.line_start[0] - self.line_end[0])

       

        cent_y = (self.line_start[1] + self.line_end[1])//2
        cent_x = (self.line_start[0] + self.line_end[0])//2
        for i in range(0,360):
            y = round(w/2 * math.cos(i) + cent_y)
            x = round(h/2 * math.sin(i) + cent_x)
            self.parent.setGridPixel(x, y)
        
    
    


