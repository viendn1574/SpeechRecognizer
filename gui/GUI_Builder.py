import csv

try:
    from Tkinter import *
except ImportError:
    from Tkinter import *

try:
    import ttk
    py3 = False
except ImportError:
    import tkinter.ttk as ttk
    py3 = True

import feature_support
import NeuralNetwork


def vp_start_gui():
    '''Starting point when module is the main routine.'''
    with open('list_person.txt','r') as csvfile:
        reader=csv.reader(csvfile, delimiter=' ')
        row_count = sum(1 for row in reader)
        if (row_count>0):
            #NeuralNetwork.init_NeuralNetwork()
            NeuralNetwork.init_dataset()
    global root
    root = Tk()
    root.resizable(False,False)
    global val, w
    top = New_Toplevel (root)
    feature_support.init(root, top)
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

        self.Frame1 = Frame(top)
        self.Frame1.place(relx=0.02, rely=0.02, relheight=0.8, relwidth=0.75)
        self.Frame1.configure(relief=GROOVE)
        self.Frame1.configure(borderwidth="2")
        self.Frame1.configure(relief=GROOVE)
        self.Frame1.configure(background="#d9d9d9")
        self.Frame1.configure(highlightbackground="#d9d9d9")
        self.Frame1.configure(highlightcolor="black")
        self.Frame1.configure(width=455)

        self.Button1 = Button(top)
        self.Button1.place(relx=0.41, rely=0.9, height=24, width=70)
        self.Button1.configure(activebackground="#d9d9d9")
        self.Button1.configure(activeforeground="#000000")
        self.Button1.configure(background="#d9d9d9")
        self.Button1.configure(command=lambda: feature_support.CancleAdd_click(self.Label1))
        self.Button1.configure(disabledforeground="#a3a3a3")
        self.Button1.configure(foreground="#000000")
        self.Button1.configure(highlightbackground="#d9d9d9")
        self.Button1.configure(highlightcolor="black")
        self.Button1.configure(pady="0")
        self.Button1.configure(text='''Cancle add''')



        self.Button4 = Button(top)
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
        self.Button4.config(state=DISABLED)

        self.Button3 = Button(top)
        self.Button3.place(relx=0.8, rely=0.02, height=24, width=44)
        self.Button3.configure(activebackground="#d9d9d9")
        self.Button3.configure(activeforeground="#000000")
        self.Button3.configure(background="#d9d9d9")
        self.Button3.configure(command=lambda: feature_support.Login_click(self.Button4))
        self.Button3.configure(disabledforeground="#a3a3a3")
        self.Button3.configure(foreground="#000000")
        self.Button3.configure(highlightbackground="#d9d9d9")
        self.Button3.configure(highlightcolor="black")
        self.Button3.configure(pady="0")
        self.Button3.configure(text="Log in")

        self.Label1=Label(top,text="")
        self.Label1.place(relx=0.021,rely=0.85)

        self.Button2 = Button(top)
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
    

if __name__ == '__main__':

    vp_start_gui()











