import vlc
import sys
import tkinter as Tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename

import os
import pathlib
from threading import Timer,Thread,Event
import time
import platform
import cv2
import dlib
import threading
global s

s=0


class ttkTimer(Thread):
    def __init__(self, callback, tick):
        Thread.__init__(self)
        self.callback = callback
        #print("callback= ", callback())
        self.stopFlag = Event()
        self.tick = tick
        self.iters = 0

    def run(self):
        while not self.stopFlag.wait(self.tick):
            self.iters += 1
            self.callback()
            #print("ttkTimer start")

    def stop(self):
        self.stopFlag.set()

    def get(self):
        return self.iters

class Player(Tk.Frame):

    def __init__(self, parent=None, title=None):
        Tk.Frame.__init__(self, parent)
    
        self.parent = parent

        if title == None:
            title = "tk_vlc"
        self.parent.title(title)
        menubar = Tk.Menu(self.parent,background='#374140', foreground='white',activebackground='#374140', activeforeground='white',font=('Tempus Sans ITC', 14))
        
        self.parent.config(bg='#2A2C2B',menu=menubar)

        fileMenu = Tk.Menu(menubar, tearoff=0, background='#374140',foreground='White', activebackground='blue',activeforeground='white')
        fileMenu.add_command(label="Open", underline=0, font=("Arial 13 "),command=self.OnOpen)
        fileMenu.add_separator()
        fileMenu.add_command(label="Exit", underline=1, font=("Arial 13 "),command=_quit)
        menubar.add_cascade(label=" MEDIA ", menu=fileMenu)
     
        
        self.player = None
        self.videopanel = ttk.Frame(self.parent)
        self.canvas = Tk.Canvas(self.videopanel,bg="black", bd=0, highlightthickness=0, relief='ridge').pack(fill=Tk.BOTH,expand=1)
        
        self.videopanel.pack(fill=Tk.BOTH,expand=1)

        ctrlpanel = ttk.Frame(self.parent)
        #ctrlpanel.pack(side=Tk.BOTTOM)

        ctrlpanel2 = ttk.Frame(self.parent)
        self.scale_var = Tk.DoubleVar()
        self.timeslider_last_val = ""
        self.timeslider = Tk.Scale(ctrlpanel2, variable=self.scale_var, command=self.scale_sel,from_=0, to=1000, orient=Tk.HORIZONTAL, length=500)
        self.timeslider.pack(side=Tk.BOTTOM, fill=Tk.X,expand=1)
        self.timeslider.pack(side=Tk.BOTTOM, fill=Tk.X,expand=1)
        self.timeslider_last_update = time.time()
        ctrlpanel2.pack(side=Tk.BOTTOM,fill=Tk.X)
        

        self.Instance = vlc.Instance()
        self.player = self.Instance.media_player_new()

        self.timer = ttkTimer(self.OnTimer, 1.0)
        self.timer.start()
        self.parent.update()

        




    def OnExit(self, evt):
         print ('switch off')  
         global switch  
         switch = False
         #self.Close()

    def OnOpen(self):
        global switch 
        if(s==0):
            switch=False  
        self.OnStop()
        switch = True
        #if(flag==1):
         #   thread._stop()
            
        p = pathlib.Path(os.path.expanduser("~"))
        fullname =  askopenfilename(initialdir = p, title = "choose your file",filetypes = (("all files","*.*"),("mp4 files","*.mp4")))
        if os.path.isfile(fullname):
            print (fullname)
            splt = os.path.split(fullname)
            dirname  = os.path.dirname(fullname)
            filename = os.path.basename(fullname)
           
            self.Media = self.Instance.media_new(str(os.path.join(dirname, filename)))
            self.player.set_media(self.Media)
            
            if platform.system() == 'Windows':
                self.player.set_hwnd(self.GetHandle())
            else:
                self.player.set_xwindow(self.GetHandle())
            
            self.detectAndTrackLargestFace()
    def OnTimer(self):
        
        if self.player == None:
            return
        
        length = self.player.get_length()
        dbl = length * 0.001
        self.timeslider.config(to=dbl)

        
        tyme = self.player.get_time()
        if tyme == -1:
            tyme = 0
        dbl = tyme * 0.001
        self.timeslider_last_val = ("%.0f" % dbl) + ".0"
        
        if time.time() > (self.timeslider_last_update + 2.0):
            self.timeslider.set(dbl)

    def scale_sel(self, evt):
        if self.player == None:
            return
        nval = self.scale_var.get()
        sval = str(nval)
        if self.timeslider_last_val != sval:
    
            self.timeslider_last_update = time.time()
            mval = "%.0f" % (nval * 1000)
            self.player.set_time(int(mval)) # expects milliseconds

    

    def OnPlay(self):
        
        if not self.player.get_media():
            self.OnOpen()
        else:
            
            if self.player.play() == -1:
                self.errorDialog("Unable to play.")

    def GetHandle(self):
        return self.videopanel.winfo_id()

    
    def OnPause(self):

        self.player.pause()

    def OnStop(self):

        self.player.stop()
    
    

    def errorDialog(self, errormessage):

        edialog = Tk.tkMessageBox.showerror(self, 'Error', errormessage)
    def detectAndTrackLargestFace(self):
         def run():

            faceCascade = cv2.CascadeClassifier('C:\\Users\\abc\\AppData\\Local\\\Programs\\Python\\Python36-32\\Lib\\site-packages\\cv2\\data\\haarcascade_frontalface_default.xml')
            OUTPUT_SIZE_WIDTH = 200
            OUTPUT_SIZE_HEIGHT = 200

 
            capture = cv2.VideoCapture(0)
            cv2.namedWindow("base-image", cv2.WINDOW_AUTOSIZE)
            cv2.namedWindow("result-image", cv2.WINDOW_AUTOSIZE)

   
            cv2.moveWindow("base-image",900,900)
            cv2.moveWindow("result-image",0,500)


            cv2.startWindowThread()
            tracker = dlib.correlation_tracker()
            trackingFace = 0
            
            rectangleColor = (0,165,255)


            try:
                while (switch== True):
                    
                    
                    rc,fullSizeBaseImage = capture.read()
                    
                    baseImage = cv2.resize( fullSizeBaseImage, ( 320, 240))
       
                    pressedKey = cv2.waitKey(2)
                    
                    if pressedKey == ord('Q'):
                        cv2.destroyAllWindows()
                        exit(0)

                    resultImage = baseImage.copy()

                    time.sleep(0.001)
                    

                    
                    if switch == False:  
                        break  
                    if not trackingFace:
                        
                         
                        RgbImage = cv2.cvtColor(baseImage, cv2.COLOR_BGR2GRAY)
                        faces = faceCascade.detectMultiScale(RgbImage, 1.3, 5)
        
                        print("Using the cascade detector to detect face")
                        


                        maxArea = 0
                        x = 0
                        y = 0
                        w = 0
                        h = 0
 
                        for (_x,_y,_w,_h) in faces:
                            if  _w*_h > maxArea:
                                x = int(_x)
                                y = int(_y)
                                w = int(_w)
                                h = int(_h)
                                maxArea = w*h


                        if maxArea > 0 :

  
                            tracker.start_track(baseImage,
                                                dlib.rectangle( x-10,
                                                                y-20,
                                                                x+w+10,
                                                                y+h+20))


                            trackingFace = 1


                    if trackingFace:

                        trackingQuality = tracker.update( baseImage )

                        if trackingQuality >= 8.75:
                            tracked_position =  tracker.get_position()

                            t_x = int(tracked_position.left())
                            t_y = int(tracked_position.top())
                            t_w = int(tracked_position.width())
                            t_h = int(tracked_position.height())
                            cv2.rectangle(resultImage, (t_x, t_y),
                                                        (t_x + t_w , t_y + t_h),
                                                        rectangleColor ,2)
                            #print("REctangle")
                            self.OnPlay()                            

                        else:
                            self.OnPause()
                            trackingFace = 0


                    largeResult = cv2.resize(resultImage,
                                             (OUTPUT_SIZE_WIDTH,OUTPUT_SIZE_HEIGHT))

                    cv2.imshow("base-image", baseImage)
                    cv2.imshow("result-image", largeResult)
                    
                    


            except KeyboardInterrupt as e:
                cv2.destroyAllWindows()
                exit(0)

         thread = threading.Thread(target=run)  
         thread.start() 


def Tk_get_root():
    if not hasattr(Tk_get_root, "root"): 
        Tk_get_root.root= Tk.Tk()  
    return Tk_get_root.root
        
def _quit():
    print("_quit: bye")
    root = Tk_get_root()
    root.quit()     
    root.destroy()  

    os._exit(1)

if __name__ == "__main__":
    
    root = Tk_get_root()
    root.protocol("WM_DELETE_WINDOW", _quit)
    root.state('zoomed')
    
    root.wm_iconbitmap('1.ico')
    player = Player(root, title="VLC Player")
    
    root.mainloop()

