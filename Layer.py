import numpy as np
class Layer:
    id_offset = 1000
    def __init__(self, width, height, alpha):
        Layer.id_offset += 1
        self.id = Layer.id_offset
        self.content = np.zeros((height, width, 3), dtype=np.float64)
        self.alpha = np.ones((height, width), dtype=np.float64) * alpha
        self.width = width
        self.height = height
        self.visible = True
        self.layer_method = 'normal'
    def normal(self, base):
        if not self.visible: return base
        ret = self.content * self.alpha[:,:,np.newaxis] + base * (np.ones((self.height, self.width), dtype = np.float64)*255 -  self.alpha)[:,:,np.newaxis]
        ret = ret / 255
        return ret.astype(np.uint8)
    def normal_pixel(self, base, x, y):
        if not self.visible: return base
        ret = self.content[x][y] * self.alpha[x][y] + base * (255 - self.alpha[x][y])
        ret = ret/255
        return ret.astype(np.uint8)