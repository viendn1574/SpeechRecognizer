import gc

import pygame
import GUI_Builder
import Tkinter
import matplotlib
import RPi.GPIO as GPIO
matplotlib.use('TkAgg')

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import feature_support
import NeuralNetwork

GUI_Builder.object=None
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(18,GPIO.IN,pull_up_down=GPIO.PUD_UP)

def vp_start_gui():
    '''Starting point when module is the main routine.'''
    with open('./data/list_person.txt','r') as lpfile:
        row_count = sum(1 for row in lpfile)
        if (row_count>0):
            NeuralNetwork.init_model()
            #NeuralNetwork.init_dataset()
    root = Tkinter.Tk()
    root.resizable(False,False)
    GUI_Builder.object = New_Toplevel (root)
    root.mainloop()


class New_Toplevel:

    def __init__(self, top=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9' # X11 color: 'gray85'
        _ana1color = '#d9d9d9' # X11 color: 'gray85'
        _ana2color = '#d9d9d9' # X11 color: 'gray85'

        top.geometry("603x421+533+155")
        top.title("New Toplevel")
        top.configure(background="#d9d9d9")
        top.configure(highlightbackground="#d9d9d9")
        top.configure(highlightcolor="black")

        self.Frame1 = Tkinter.Frame(top)
        self.Frame1.place(relx=0.02, rely=0.02, relheight=0.8, relwidth=0.75)
        self.Frame1.configure(relief=Tkinter.GROOVE)
        self.Frame1.configure(borderwidth="2")
        self.Frame1.configure(relief=Tkinter.GROOVE)
        self.Frame1.configure(background="#d9d9d9")
        self.Frame1.configure(highlightbackground="#d9d9d9")
        self.Frame1.configure(highlightcolor="black")
        self.Frame1.configure(width=455)

        self.Button1 = Tkinter.Button(top)
        self.Button1.place(relx=0.41, rely=0.9, height=24, width=70)
        self.Button1.configure(activebackground="#d9d9d9")
        self.Button1.configure(activeforeground="#000000")
        self.Button1.configure(background="#d9d9d9")
        self.Button1.configure(command=feature_support.CancleAdd_click)
        self.Button1.configure(disabledforeground="#a3a3a3")
        self.Button1.configure(foreground="#000000")
        self.Button1.configure(highlightbackground="#d9d9d9")
        self.Button1.configure(highlightcolor="black")
        self.Button1.configure(pady="0")
        self.Button1.configure(text='''Cancle add''')
        self.Button1.config(state=Tkinter.DISABLED)


        self.Button4 = Tkinter.Button(top)
        self.Button4.place(relx=0.9, rely=0.02, height=24, width=49)
        self.Button4.configure(activebackground="#d9d9d9")
        self.Button4.configure(activeforeground="#000000")
        self.Button4.configure(background="#d9d9d9")
        self.Button4.configure(command=feature_support.List_click)
        self.Button4.configure(disabledforeground="#a3a3a3")
        self.Button4.configure(foreground="#000000")
        self.Button4.configure(highlightbackground="#d9d9d9")
        self.Button4.configure(highlightcolor="black")
        self.Button4.configure(pady="0")
        self.Button4.configure(text='''List''')
        self.Button4.config(state=Tkinter.DISABLED)

        self.ButtonConfig = Tkinter.Button(top)
        self.ButtonConfig.place(relx=0.9, rely=0.1, height=24, width=49)
        self.ButtonConfig.configure(activebackground="#d9d9d9")
        self.ButtonConfig.configure(activeforeground="#000000")
        self.ButtonConfig.configure(background="#d9d9d9")
        self.ButtonConfig.configure(command=feature_support.Setting_click)
        self.ButtonConfig.configure(disabledforeground="#a3a3a3")
        self.ButtonConfig.configure(foreground="#000000")
        self.ButtonConfig.configure(highlightbackground="#d9d9d9")
        self.ButtonConfig.configure(highlightcolor="black")
        self.ButtonConfig.configure(pady="0")
        self.ButtonConfig.configure(text='''Setting''')
        self.ButtonConfig.config(state=Tkinter.DISABLED)

        self.Button3 = Tkinter.Button(top)
        self.Button3.place(relx=0.8, rely=0.02, height=24, width=55)
        self.Button3.configure(activebackground="#d9d9d9")
        self.Button3.configure(activeforeground="#000000")
        self.Button3.configure(background="#d9d9d9")
        self.Button3.configure(command=lambda: feature_support.Login_click(self.Button3,self.Button4))
        self.Button3.configure(disabledforeground="#a3a3a3")
        self.Button3.configure(foreground="#000000")
        self.Button3.configure(highlightbackground="#d9d9d9")
        self.Button3.configure(highlightcolor="black")
        self.Button3.configure(pady="0")
        self.Button3.configure(text="Log in")

        self.Label1= Tkinter.Label(top, text="")
        self.Label1.place(relx=0.021,rely=0.85)

        self.Button2 = Tkinter.Button(top)
        self.Button2.place(relx=0.28, rely=0.9, height=24, width=48)
        self.Button2.configure(activebackground="#d9d9d9")
        self.Button2.configure(activeforeground="#000000")
        self.Button2.configure(background="#d9d9d9")
        self.Button2.configure(disabledforeground="#a3a3a3")
        self.Button2.configure(foreground="#000000")
        self.Button2.configure(highlightbackground="#d9d9d9")
        self.Button2.configure(highlightcolor="black")
        self.Button2.configure(pady="0")
        self.Button2.configure(text='''Record''')
        self.Button2.bind('<ButtonPress-1>',lambda event, Label1=self.Label1:  feature_support.Record_click(event,Label1))
        self.Button2.bind('<ButtonRelease-1>',lambda event, Label1=self.Label1: feature_support.Record_release(event,Label1))
        self.f = Figure( figsize=(10, 9), dpi=80 )
        self.a = self.f.add_subplot(211)
        self.b =self.f.add_subplot(212)
        self.f.clf()
        self.canvas = FigureCanvasTkAgg(self.f, master=self.Frame1)
        self.canvas.get_tk_widget().pack(side=Tkinter.TOP, fill=Tkinter.BOTH, expand=1)
        self.root=top
        self.afterid= self.root.after(5000,self.update_clock)
        GPIO.add_event_detect(18, GPIO.FALLING, callback=lambda event, Label1=self.Label1:  feature_support.Record_click(event,Label1), bouncetime=200)


    def canvas_show(self,sig,mfcc):
        self.root.after_cancel(self.afterid)

        self.f.add_axes(self.a)
        self.f.add_axes(self.b)
        self.a.clear()
        self.b.clear()
        self.a.plot(sig)
        self.b.plot(mfcc)
        self.canvas.draw()
        self.afterid=self.root.after(5000,self.update_clock)
        gc.collect()
        return
    def update_clock(self):

        self.Label1.configure(text="")
        self.f.clf()
        self.canvas.draw()
        active = pygame.mixer.get_init()

        if active != None:
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
            pygame.mixer.music.stop()
            pygame.mixer.quit()
            pygame.quit()
        gc.collect()

        self.afterid= self.root.after(5000,self.update_clock)
if __name__ == '__main__':
    vp_start_gui()











