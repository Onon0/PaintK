import math
class Brush:
    def __init__(self):
        self.size = 10
    def getBrushArea(self, pos_x, pos_y):
        arr = []
        for i in range(pos_x - self.size, pos_x + self.size):
            for j in range(pos_y - self.size, pos_y + self.size):
                dist = math.sqrt(((pos_x - i)**2 + (pos_y - j)**2))
            
                if(dist <= self.size):
                    arr.append([i,j])
        return arr
