from tkinter import ttk,Tk,Text,filedialog,font,messagebox
from tkinter import *
from camASCII import VideoToAscii
import cv2 

class CameraGui():
    frameMS=16

    def __init__(self,parent):
        self.mainframe = ttk.Frame(parent)
        self.mainframe.grid(column=0,row=0,sticky=(N,W,S,E))
        self.FixedFont = font.nametofont("TkFixedFont")
        self.filePath = StringVar()
        self.newWidth = StringVar()
        ttk.Label(self.mainframe,text="Filepath (mp4):").grid(column=1,row=1,sticky=E)
        ttk.Entry(self.mainframe,textvariable=self.filePath).grid(column=2,row=1,sticky=[W,E],padx=10,pady=10)
        
        ttk.Button(self.mainframe,text="Browse",command=self.Browse).grid(column=3,row=1,sticky=W,padx=10,pady=10)
        ttk.Button(self.mainframe,text="From File",command=self.asciiToGUI).grid(column=4,row=1, sticky=[W,E],pady=10)
        self.cameraButton=ttk.Button(self.mainframe,text="From Camera",command=self.cameraToAscii)
        self.cameraButton.grid(column=4,row=2, sticky=[W,E],pady=10)
        ttk.Button(self.mainframe,text="Stop",command=self.Stop).grid(column=5,row=1, sticky=W,pady=10,padx=10)
        ttk.Label(self.mainframe,text="Width (up to 250):").grid(column=1,row=2,sticky=E)
        ttk.Entry(self.mainframe,textvariable=self.newWidth).grid(column=2,row=2,sticky=[W,E],padx=10,pady=10)
        
        self.asciiView=Text(self.mainframe,font=self.FixedFont)
        self.asciiView.grid(columnspan=5,column=1,row=3 ,sticky=N)


    def asciiToGUI(self):
        try:
            self.cap=cv2.VideoCapture(self.filePath.get())
            self.resizeTextWidget()
            self.width=self.getEntryWidth()
            self.frameMS=round(1000/self.cap.get(cv2.CAP_PROP_FPS))
            self.asciiView.after(self.frameMS,self.setText)
        except:
            messagebox.showerror(title="No Filepath",message="No File was Found in Path")
    
    def cameraToAscii(self):
            self.disableCameraButton()
            self.cap=cv2.VideoCapture(0)
            self.resizeTextWidget()
            self.width=self.getEntryWidth()
            self.frameMS=round(1000/self.cap.get(cv2.CAP_PROP_FPS))
            self.asciiView.after(self.frameMS,self.setText)
            

    
    def setText(self):
        if self.cap.isOpened():
            ret,frame = self.cap.read()
            if ret:
                self.asciiView.delete(1.0,END)
                self.asciiView.insert(END,VideoToAscii(frame,self.width))
                self.asciiView.after(self.frameMS,self.setText)
            else:
                self.cap.release()
                
    def disableCameraButton(self):
        self.cameraButton["state"]=DISABLED
    def enableCameraButton(self):
        self.cameraButton["state"]=NORMAL
        
    def Stop(self):
        self.enableCameraButton()
        self.cap.release()
            

    def resizeTextWidget(self):
        new_width=self.getEntryWidth()
        original_height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        original_width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        ratio = original_height / original_width
        
        new_height = int(new_width * ratio * 0.35)
        self.asciiView["width"]=new_width
        self.asciiView["height"]=new_height

    def Browse(self):
        self.filePath.set(filedialog.askopenfilename())
    
    def getEntryWidth(self):
        if self.newWidth.get().isnumeric():
            new_width=int(self.newWidth.get())
        else:
            new_width=100
        return new_width
        

            
root = Tk()
crass=CameraGui(root)
root.mainloop()