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

        

        self.layerList = ctk.CTkScrollableFrame(self, width = 250, height= 30)
        self.AddLayerBtn = tk.Button(self, text="+", width= 3, height=3, command=self.AddLayer)
        
        self.layerList.pack(side=tk.TOP)
        tk.Frame(self, bg="red", height=50).pack(side=tk.TOP)
        self.AddLayerBtn.place(relx=1.0, rely=1.0, anchor="se")
    def AddLayer(self):
        newLayer = Layer(self.parent.width, self.parent.height)
        print(f"width: {self.parent.width} height: {self.parent.height}")
        LayerItem(self.layerList, newLayer, self).pack(side=tk.BOTTOM)
        self.parent.layers.append(newLayer)
        if len(self.parent.layers) == 1: self.setLayer(self.parent.layers[0].id)
        self.parent.UpdateLayers()
        self.parent.UpdateDisplay()
    
    def setLayer(self, index):
        
        print("selected" + str(index))
        for child_name, child in self.layerList.children.items():
            if child.layer.id == index:
                child.setColor("green")
            else:
                child.setColor("red")
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
    def toggleOnionVisibility(self, index):
        pass

    def removeLayer(self, index):
        
        for i in range(len(self.parent.layers)):
            if(self.parent.layers[i].id == index):
                del self.parent.layers[i]
                if len(self.parent.layers) > 0 : 
                    self.setLayer(self.parent.layers[0].id)
                self.parent.UpdateLayers()
                self.parent.UpdateDisplay()
                break
    
    def moveUp(self, index):
        for i in range(len(self.parent.layers)):
            if(self.parent.layers[i].id == index):
                if i+1 >= len(self.parent.layers):
                    return
                temp = self.parent.layers[i]
                self.parent.layers[i] = self.parent.layers[i + 1]
                self.parent.layers[i + 1] = temp
                self.parent.UpdateLayers()
                self.parent.UpdateDisplay()
                self.refreshLayerItems()
                return
    def moveDown(self, index):
        for i in range(len(self.parent.layers)):
            if(self.parent.layers[i].id == index):
                if i == 0:
                    return
                temp = self.parent.layers[i]
                self.parent.layers[i] = self.parent.layers[i - 1]
                self.parent.layers[i - 1] = temp
                self.parent.UpdateLayers()
                self.parent.UpdateDisplay()
                self.refreshLayerItems()
                return
    def refreshLayerItems(self):
        for widget in self.layerList.winfo_children():
            widget.destroy()
        for l in self.parent.layers:
            LayerItem(self.layerList, l, self).pack(side=tk.BOTTOM)
        if len(self.parent.layers) > 0 :
            self.setLayer(self.parent.layers[0].id)
class LayerItem(tk.Frame):
    def __init__(self, root, layer, parent, **kwargs):
        super().__init__(root, **kwargs)
        self.parent = parent
        self.layer = layer
        self.LayerButton = tk.Button(self, text = self.layer.name, width= 20, bg="red" )
        self.LayerButton.config(command=lambda idx = self.layer.id: self.selectLayer(idx) )
        self.LayerButton.grid(column=0, row=0)
        tk.Button(self, text = "B", width= 5, command=lambda idx = self.layer.id: self.parent.toggleLayerVisibility(idx)).grid(column=1, row=0)
        tk.Button(self, text = "O", width= 5, command=lambda idx = self.layer.id: self.parent.toggleOnionVisibility(idx)).grid(column=2, row=0)
        
        self.contextMenu = tk.Menu(self.LayerButton, tearoff=0)
        self.contextMenu.add_command(label="delete layer", command=self.deleteLayer)
        self.contextMenu.add_command(label="move up", command=self.move_up)
        self.contextMenu.add_command(label="move down", command=self.move_down)
        
        self.LayerButton.bind("<Button-3>", self.show_context_menu)
    def setColor(self, color):
        self.LayerButton.config(bg=color)
    
    def selectLayer(self, _id):
        self.parent.setLayer(_id)

    def deleteLayer(self):
        self.parent.removeLayer(self.layer.id)
        self.pack_forget()
    def move_up(self):
        self.parent.moveUp(self.layer.id)
    def move_down(self):
        self.parent.moveDown(self.layer.id)
    def show_context_menu(self, event):
        try:
            self.contextMenu.tk_popup(event.x_root, event.y_root)
        finally:
            self.contextMenu.grab_release() # Release the grab when an item is selected