import tkinter as tk
from tkinter.ttk import *
import customtkinter as ctk
from PIL import Image, ImageTk
import numpy as np
import time
import threading
from DataStructs import Layer
from Tools import *
class AnimationModule(tk.Frame):
    def __init__(self, root, parent,  **kwargs):
        super().__init__(root, **kwargs)
        self.parent = parent
        self.isPlaying = False
        self.frameContainer = ctk.CTkScrollableFrame(self, width = 500, height= 100, orientation="horizontal")
        self.keyFrameModules = []
        for i in range(250):
            #tk.Button(self.frameContainer, width=5, height=20, command= lambda idx = i: self.LoadFrame(idx)).grid(column=i,row= 0)
            kfm = KeyFrameModule(self.frameContainer, i, self)
            kfm.grid(column=i, row=0)
            self.keyFrameModules.append(kfm)
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
    def unSelectLast(self):
        self.keyFrameModules[self.parent.currentFrameIndex].setSelected(False)
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
            #print("playing" + str(i))
            self.keyFrameModules[self.parent.currentFrameIndex].setSelected(False)
            self.LoadFrame(i)
            self.keyFrameModules[i].setSelected(True)
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
class KeyFrameModule(tk.Frame):
    def __init__(self, root, frame_id, parent_module,  **kwargs):
        super().__init__(root, **kwargs)
        self.frame_id = frame_id
        self.parent_module = parent_module
        self.frame_label_container = tk.Frame(self, width=5, height = 5, background="red")
        self.frame_label_container.pack()
        tk.Label(self.frame_label_container, text=f"{self.frame_id}").pack()
        self.btn = tk.Button(self, width=5, height=20, command = self.OnKeyframeSelected)
        self.btn.pack()
    def setSelected(self, is_selected = False):
        if is_selected:
            self.btn.configure(relief = tk.SUNKEN)
        else:
            self.btn.configure(relief = tk.RAISED)
    def OnKeyframeSelected(self):
        self.parent_module.unSelectLast()
        self.setSelected(True)
        self.parent_module.LoadFrame(self.frame_id)
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
        
        self.opacity = tk.Scale(self , label="opacity" , from_=0, to=255, orient=tk.HORIZONTAL, command=self.updateCanvas)
        self.opacity.pack()
        self.opacity.set(255)
        self.canvas_color = np.ones((100,100, 3), dtype = np.uint8 )
        img = Image.fromarray(self.canvas_color)
        self.photo_img = ImageTk.PhotoImage(image=img)
        self.image_element = self.canvas.create_image(1,1,image=self.photo_img, anchor="nw")

        self.currentColor = [self.red.get(),self.green.get(),self.blue.get()]
    def updateCanvas(self, value):
        #[1,1,1] * current color
        self.canvas_color =np.multiply( np.ones((100,100, 3) ), np.array([self.red.get(),self.green.get(),self.blue.get()]))
        self.opacity_value = self.opacity.get()
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
        
        for child_name, child in self.layerList.children.items():
            if child.layer.id == index:
                child.setRelief(tk.SUNKEN)
            else:
                child.setRelief(tk.RAISED)
        for i in range(len(self.parent.layers)):
            if(self.parent.layers[i].id == index):
                self.parent.currentLayerIndex = i
                break
    def refreshLayers(self):
        
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
        self.LayerButton = tk.Button(self, text = self.layer.name, width= 20, relief=tk.RAISED )
        self.LayerButton.config(command=lambda idx = self.layer.id: self.selectLayer(idx) )
        self.LayerButton.grid(column=0, row=0)
        original_image = Image.open("layer_visible_icon.png")
        resized_image = original_image.resize((25, 25)) 

        self.visible_icon = ImageTk.PhotoImage(resized_image)
        self.btn_visibility = tk.Button(self, image=self.visible_icon, width= 25, height=25, command=self.toggleVisibility)
        self.btn_visibility.grid(column=1, row=0)
        self.btn_onion = tk.Button(self, text = "O", width= 5, command=self.toggleOnionVisibility)
        self.btn_onion.grid(column=2, row=0)
        self.contextMenu = tk.Menu(self.LayerButton, tearoff=0)
        self.contextMenu.add_command(label="delete layer", command=self.deleteLayer)
        self.contextMenu.add_command(label="move up", command=self.move_up)
        self.contextMenu.add_command(label="move down", command=self.move_down)
        
        self.LayerButton.bind("<Button-3>", self.show_context_menu)
    def setRelief(self, relief):
        self.LayerButton.config(relief=relief)
    def toggleVisibility(self):
        self.layer.visible = not self.layer.visible
        self.parent.refreshLayers()
        if self.layer.visible:
            self.btn_visibility.configure(relief=tk.RAISED)
        else:
            self.btn_visibility.configure(relief=tk.SUNKEN)
    def toggleOnionVisibility(self):
        self.layer.onion_visible = not self.layer.onion_visible
        self.parent.refreshLayers()
        if self.layer.onion_visible:
            self.btn_onion.configure(relief=tk.RAISED)
        else:
            self.btn_onion.configure(relief=tk.SUNKEN)
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

class ToolsModule(tk.Frame):
    def __init__(self, root, parent,  **kwargs):
        super().__init__(root, **kwargs)
        self.parent = parent
        
        
        self.buttons = []
        self.brush_icon = self.load_icon(path = r'icons/brush_icon.png')
        self.eraser_icon = self.load_icon(path = r'icons/eraser_icon.png')
        self.line_icon = self.load_icon(path = r'icons/line_icon.png')
        self.box_icon = self.load_icon(path = r'icons/box_icon.png')
        self.circle_icon = self.load_icon(path = r'icons/circle_icon.png')
        
        # Convert to Tkinter PhotoImage
        self.brush_btn = self.addToolButton(self.setBrush,self.brush_icon, is_default=True)
        self.eraser_btn =self.addToolButton(self.setEraser, self.eraser_icon, grid_at=(1,0))
        self.line_btn = self.addToolButton(self.setLine,self.line_icon, grid_at=(2,0))
        self.box_btn = self.addToolButton(self.setBox,self.box_icon, grid_at=(3,0))
        self.circle_btn = self.addToolButton(self.setCircle, self.circle_icon, grid_at=(4,0))

    def load_icon(self, path, fit_size = (50,50)):
        original_image = Image.open(path)
        resized_image = original_image.resize(fit_size) 

        return ImageTk.PhotoImage(resized_image)
    def addToolButton(self,command, icon_image, grid_at = (0,0)  ,is_default =False):
        

        btn = tk.Button(self, image= icon_image , width=50, height=50, command=command)
        if is_default:
            btn.configure(relief=tk.SUNKEN)
        btn.grid(column=grid_at[0], row=grid_at[1])
        self.buttons.append(btn)
        return btn
    def unselectAll(self):
        for btn in self.buttons:
            btn.configure(relief = tk.RAISED)
    def setBrush(self):
        self.unselectAll()
        self.brush_btn.configure(relief=tk.SUNKEN)
        self.parent.tool = Brush(self.parent)
    def setEraser(self):
        self.unselectAll()
        self.eraser_btn.configure(relief=tk.SUNKEN)
        self.parent.tool = Eraser(self.parent)
    def setLine(self):
        self.unselectAll()
        self.line_btn.configure(relief=tk.SUNKEN)
        self.parent.tool = Line(self.parent)
    def setBox(self):
        self.unselectAll()
        self.box_btn.configure(relief=tk.SUNKEN)
        self.parent.tool = Box(self.parent)
    def setCircle(self):
        self.unselectAll()
        self.circle_btn.configure(relief=tk.SUNKEN)
        self.parent.tool = Circle(self.parent)