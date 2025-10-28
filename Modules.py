import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk
import numpy as np
import time
import threading
from DataStructs import Layer

class AnimationModule(tk.Frame):
    def __init__(self, root, parent,  **kwargs):
        super().__init__(root, **kwargs)
        self.parent = parent
        self.isPlaying = False
        self.frameContainer = ctk.CTkScrollableFrame(self, width = 500, height= 100, orientation="horizontal")
        for i in range(250):
            tk.Button(self.frameContainer, width=5, height=20, command= lambda idx = i: self.LoadFrame(idx)).grid(column=i,row= 0)
        self.controlContainer = tk.Frame(self)
        
        self.playBtn = tk.Button(self.controlContainer, width= 5, command= self.startAnimationThread).pack(side=tk.LEFT)
        #self.pauseBtn = tk.Button(self.controlContainer, width= 5, command= self.stopAnimation).pack(side=tk.LEFT)
        self.frameContainer.pack(side = tk.TOP)
        self.controlContainer.pack(side = tk.TOP)
    def LoadFrame(self, i):
        #print("current frame is "+ str(i))
        self.parent.currentFrameIndex = i
        self.parent.UpdateLayers()
        self.parent.UpdateDisplay()
    def startAnimationThread(self):
        
        if self.isPlaying:
            print("stop animation called")
            self.stopAnimation()
        else:
            self.isPlaying = True
            self.anim_thread = threading.Thread(target=self.playAnimation)
            self.anim_thread.start()
        
    def playAnimation(self):
        i = 0
        while self.isPlaying:
            print("playing" + str(i))
            
            self.LoadFrame(i)
            i+=1
            if i > 10:
                i = 0

            time.sleep(1/24)
        print("Animation loop stopped")
        
    def stopAnimation(self):
        
        print("loop set to false")
        self.isPlaying = False
        print("joining thread")
        self.anim_thread.join(timeout=5)
        print("stopping animation")
class ColorPalette(tk.Frame):
    def __init__(self, root,  **kwargs):
        super().__init__(root, **kwargs)
        
        self.canvas = tk.Canvas(self, width=100, height=100)
        
        self.canvas.pack(side=tk.TOP)

        self.red = tk.Scale(self, label="red", from_=0, to=255, orient=tk.HORIZONTAL, command=self.updateCanvas)
        self.red.pack()
        self.green = tk.Scale(self, label="green" , from_=0, to=255, orient=tk.HORIZONTAL, command=self.updateCanvas)
        self.green.pack()
        self.blue = tk.Scale(self , label="blue" , from_=0, to=255, orient=tk.HORIZONTAL, command=self.updateCanvas)
        self.blue.pack()

        self.canvas_color = np.ones((100,100, 3), dtype = np.uint8 )
        img = Image.fromarray(self.canvas_color)
        self.photo_img = ImageTk.PhotoImage(image=img)
        self.image_element = self.canvas.create_image(1,1,image=self.photo_img, anchor="nw")

        self.currentColor = [self.red.get(),self.green.get(),self.blue.get()]
    def updateCanvas(self, value):
        #[1,1,1] * current color
        self.canvas_color =np.multiply( np.ones((100,100, 3) ), np.array([self.red.get(),self.green.get(),self.blue.get()]))
        img = Image.fromarray(self.canvas_color.astype(np.uint8))
        self.photo_img = ImageTk.PhotoImage(image=img)
        self.canvas.itemconfig(self.image_element, image = self.photo_img)
        self.currentColor = [self.red.get(),self.green.get(),self.blue.get()]


class LayerModule(tk.Frame):
    def __init__(self, root, parent,  **kwargs):
        super().__init__(root, **kwargs)
        self.parent = parent

        

        self.layerList = ctk.CTkScrollableFrame(self, width = 200, height= 30)
        self.AddLayerBtn = tk.Button(self, text="+", width= 3, height=3, command=self.AddLayer)
        
        self.layerList.pack(side=tk.TOP)
        tk.Frame(self, bg="red", height=50).pack(side=tk.TOP)
        self.AddLayerBtn.place(relx=1.0, rely=1.0, anchor="se")
    def AddLayer(self):
        newLayer = Layer(self.parent.width, self.parent.height)
        
        tk.Button(self.layerList, text = "Layer"+ str(newLayer.id), width= 20, command=lambda idx = newLayer.id: self.setLayer(idx)  ).grid(column=0,row= 200 - len(self.parent.layers))
        tk.Button(self.layerList, text = "B", width= 5, command=lambda idx = newLayer.id: self.toggleLayerVisibility(idx)).grid(column=1,row=200 - len(self.parent.layers))
        self.parent.layers.append(newLayer)
        self.parent.UpdateLayers()
        self.parent.UpdateDisplay()
    
    def setLayer(self, index):
        
        for i in range(len(self.parent.layers)):
            if(self.parent.layers[i].id == index):
                self.parent.currentLayerIndex = i
                break
    def toggleLayerVisibility(self, index):
        #print("toggling: " + str(index))
        for i in range(len(self.parent.layers)):
            if(self.parent.layers[i].id == index):
                self.parent.layers[i].visible = not self.parent.layers[i].visible 
                break
        self.parent.UpdateLayers()
        self.parent.UpdateDisplay()


