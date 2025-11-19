import numpy as np
class Layer:
    id_offset = 1000
    def __init__(self, width, height):
        Layer.id_offset += 1
        self.id = Layer.id_offset
        self.name = "Layer" + str(self.id)
        self.width = width
        self.height = height
        self.visible = True
        self.onion_visible = True
        self.__frame_header = LinkedFrame(0, owner_layer = self)
        self.frame_pointer = self.__frame_header
        
        
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
    def normal_area(self, base, top_left, bottom_right):
        if not self.visible: return base
        ret = self.frame_pointer.content[top_left[0]: bottom_right[0], top_left[1]: bottom_right[1]] \
            * self.frame_pointer.alpha[top_left[0]: bottom_right[0], top_left[1]: bottom_right[1],np.newaxis]  \
            + base\
            * (255 - self.frame_pointer.alpha[top_left[0]: bottom_right[0], top_left[1]: bottom_right[1], np.newaxis])
        ret = ret/255
        return ret.astype(np.uint8)
    def get_header(self):
        return self.__frame_header
    def find_frame(self, f_id):
        temp = self.__frame_header
        while temp != None:
            if temp.getID() > f_id:
                self.frame_pointer = temp.getPrev()
                return self.frame_pointer
            elif temp.getID() == f_id:
                self.frame_pointer = temp
                return self.frame_pointer
            temp = temp.getNext()
        return self
    def get_onion(self):
        if not self.onion_visible:
            return None
        prev = self.frame_pointer.getPrev()
        if prev == None:
            return None
        onion_frame = prev.copy()
        onion_frame.alpha = onion_frame.alpha // 2
        return onion_frame
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
    
    def __init__(self, id, owner_layer, prev = None):
        self.owner = owner_layer
        self.__id = id#id is same as frame number
        
        self.content = np.zeros((self.owner.height, self.owner.width, 3), dtype=np.float64)
        self.alpha = np.zeros((self.owner.height, self.owner.width), dtype=np.float64)
        self.__prev = prev
        self.__next = None
    #create new frame and connect
    def addNextFrame(self, id):
        newFrame = LinkedFrame(id, owner_layer= self.owner, prev = self)
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
    def copy(self):
        cp = LinkedFrame(self.__id, self.owner)
        cp.content = self.content
        cp.alpha = self.alpha
        return cp    
    def printInfo(self):
        print("--------id:" + str(self.__id))
    def normal(self, base):
        if not self.owner.visible: return base
        ret = self.content * self.alpha[:,:,np.newaxis] + base * (np.ones((self.owner.height, self.owner.width), dtype = np.float64)*255 -  self.alpha)[:,:,np.newaxis]
        ret = ret / 255
        return ret.astype(np.uint8)
    def normal_pixel(self, base, x, y):
        if not self.owner.visible: return base
        ret = self.content[x][y] * self.alpha[x][y] + base * (255 - self.alpha[x][y])
        ret = ret/255
        return ret.astype(np.uint8)
class ProjectSettings:
    def __init__(self, _name, width, height):
        self.project_name = _name
        self.width = width
        self.height = height
        
        self.layers = []
    def __str__(self):
        return f"{self.project_name}: width:{self.width}, height:{self.height}"
       
        
         
            
        
        

    