import numpy as np
class Layer:
    id_offset = 1000
    def __init__(self, width, height):
        Layer.id_offset += 1
        self.id = Layer.id_offset
        self.__frame_header = LinkedFrame(0, width=width, height=height)
        self.frame_pointer = self.__frame_header
        #self.content = np.zeros((height, width, 3), dtype=np.float64)#todo : remove after frame implementation
        #self.alpha = np.ones((height, width), dtype=np.float64) * alpha#todo : remove after frame implementation
        self.width = width
        self.height = height
        self.visible = True
        self.layer_method = 'normal'
    def normal(self, base):
        if not self.visible: return base
        ret = self.frame_pointer.content * self.frame_pointer.alpha[:,:,np.newaxis] + base * (np.ones((self.height, self.width), dtype = np.float64)*255 -  self.frame_pointer.alpha)[:,:,np.newaxis]
        ret = ret / 255
        return ret.astype(np.uint8)
    def normal_pixel(self, base, x, y):
        if not self.visible: return base
        ret = self.frame_pointer.content[x][y] * self.frame_pointer.alpha[x][y] + base * (255 - self.frame_pointer.alpha[x][y])
        ret = ret/255
        return ret.astype(np.uint8)
    def get_header(self):
        return self.__frame_header
    def find_frame(self, f_id):
        temp = self.__frame_header
        while temp != None:
            if temp.getID() > f_id:
                self.frame_pointer = temp.getPrev()
                return self
            elif temp.getID() == f_id:
                self.frame_pointer = temp
                return self
            temp = temp.getNext()
        return self
    def frame_exist(self, f_id):
        temp = self.__frame_header
        while temp != None:
            if temp.getID() == f_id:
                return True
            temp = temp.getNext()
        print("Frame doesn't exist")
        return False
    def add_frame_at(self, f_id):
        temp = self.__frame_header
        while temp != None:
            if temp.getNext() != None and temp.getNext().getID() > f_id or temp.getNext() == None:
                temp.addNextFrame(f_id)
                return
            

            temp = temp.getNext()
    def print_frame(self):
        temp = self.__frame_header
        ret = ""
        while temp != None:
            
            if self.frame_pointer.getID() == temp.getID():
                ret += "this"

            ret+=str(temp.getID()) + "->"
            
            temp = temp.getNext()
        print(ret)
class LinkedFrame:
    def __init__(self, id, width, height, prev = None):
        self.__id = id#id is same as frame number
        self.__width = width
        self.__height = height
        self.content = np.zeros((height, width, 3), dtype=np.float64)
        self.alpha = np.zeros((height, width), dtype=np.float64)
        self.__prev = prev
        self.__next = None
    #create new frame and connect
    def addNextFrame(self, id):
        newFrame = LinkedFrame(id, width= self.__width, height = self.__height, prev = self)
        if self.__next != None:
            newFrame.connectNextFrame(self.__next)
        self.__next = newFrame
    #link existing frame
    def connectNextFrame(self, nxt):
        if self.__next != None:
            nxt.connectNextFrame(self.__next)
        self.__next = nxt
        nxt.setPrev(self)
    def getID(self):
        return self.__id
    def getNext(self):
        return self.__next
    def getPrev(self):
        return self.__prev
    def setPrev(self, prev):
        self.__prev = prev
        
    def printInfo(self):
        print("--------id:" + str(self.__id))
class LayerList:
    def __init__(self):
        layers = []
       
        
         
            
        
        

    