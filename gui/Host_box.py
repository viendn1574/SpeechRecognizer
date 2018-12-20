import ttk
from Tkinter import *
import tkMessageBox
import GUI_Builder
import Host_box
import feature_support


# -- Declaration of font styles --- #
font_title = ("Helvetica", 30, "bold")
font_message = ("Helvetica", 20)
font_Entry = ("Helvetica", 20)
font_vKeyboard = ("Helvetica", 17)
font_vKeyboardSpecialKeys = ("Helvetica", 17, "bold")

# -- GUI's main class -- #
Host_box.object=None
class GUI(Toplevel):
    def __init__(self, *args, **kwargs):
        Toplevel.__init__(self, *args, **kwargs)
        
        self.geometry("%dx%d+%d+%d" % (800, 460, -1, 0))

        container = ttk.Frame(self, width=800, height=460)
        container.grid_propagate(0)
        container.pack(fill="both", expand=1)

        ttk.Style().configure("vKeyboard.TButton", font=font_vKeyboard)
        ttk.Style().configure("vKeyboardSpecial.TButton", font=font_vKeyboardSpecialKeys)

        self.frames = {}

        F=HostPage
        page_name = F.__name__
        frame = F(parent=container)
        self.frames[page_name] = frame

        frame.grid(row=0, column=0, sticky="nsew")
        self.showFrame("HostPage")
        Host_box.object=self
        self.grab_set()

    def showFrame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

class HostPage(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)
        label1 = ttk.Label(self, text="Setting Page", font=font_title)
        label1.pack(side="top", fill="x", pady=20, padx=10)

        self.label1 = ttk.Label(self, text="IP:", font=font_message)
        self.label1.pack(side="top")
        self.entry1 = ttk.Entry(self, font=font_Entry, justify=CENTER)
        self.entry1.pack(side="top")
        with open('./data/host.conf','r') as ptemp:
            person=ptemp.readline()
            self.entry1.insert(0, person)
        self.frame1 = ttk.Frame(self, width=800, height=460)
        self.frame1.pack(side="top", pady=100,padx=60)

        self.keysize = 4

        self.entry1.bind("<FocusIn>", lambda e:  self.show_vKeyboard(1))

        self.kb = vKeyboard(parentPage = self,
                            attach=self.entry1,
                            x=self.entry1.winfo_rootx(),
                            y=self.entry1.winfo_rooty() + self.entry1.winfo_reqheight(),
                            keysize=self.keysize,
                            parent=self.frame1)

    def show_vKeyboard(self, k):
        if k == 1:
            self.frame1.destroy()
            self.kb.destroy()

            self.frame1 = ttk.Frame(self, width=800, height=460)
            self.frame1.pack(side="top", pady=100,padx=60)
            self.kb = vKeyboard( parentPage = self,
                                 attach=self.entry1,
                                 x=self.entry1.winfo_rootx(),
                                 y=self.entry1.winfo_rooty() + self.entry1.winfo_reqheight(),
                                 keysize=self.keysize,
                                 parent=self.frame1)

    def get_entry(self):
        return self.entry1

class vKeyboard(ttk.Frame):
    # --- A frame for the keyboard(s) itself --- #
    def __init__(self, parentPage, parent, attach, x, y, keysize):
        ttk.Frame.__init__(self, takefocus=0)

        self.attach = attach
        self.keysize = keysize
        self.parent = parent
        self.x = x
        self.y = y
        self.parentPage = parentPage


        # --- Different sub-keyboards (e.g. alphabet, symbols..) --- #
        # --- Lowercase alphabet sub-keyboard --- #
        self.alpha_Frame = ttk.Frame(parent)
        self.alpha_Frame.grid(row=0, column=0, sticky="nsew")

        self.row1_alpha = ttk.Frame(self.alpha_Frame)
        self.row2_alpha = ttk.Frame(self.alpha_Frame)
        self.row3_alpha = ttk.Frame(self.alpha_Frame)
        self.row4_alpha = ttk.Frame(self.alpha_Frame)

        self.row1_alpha.grid(row=1)
        self.row2_alpha.grid(row=2)
        self.row3_alpha.grid(row=3)
        self.row4_alpha.grid(row=4)

        # --- Initialize all sub-keyboards --- #
        self.keyState = 1
        self.init_keys()

        self.alpha_Frame.tkraise()

        self.pack()

    def init_keys(self):
        self.alpha = {
            'row1': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0','.'],
            'row2': ['Bksp','BACK','ENTER'],
            'row3': [],
            'row4': []
        }

        self.keyStyle = self.alpha
        self.row1 = self.row1_alpha
        self.row2 = self.row2_alpha
        self.row3 = self.row3_alpha
        self.row4 = self.row4_alpha

        for row in self.keyStyle.iterkeys():  # iterate over dictionary of rows
            if row == 'row1':  # TO-DO: re-write this method
                i = 1  # for readability and functionality
                for k in self.keyStyle[row]:
                    ttk.Button(self.row1,
                               style="vKeyboard.TButton",
                               text=k,
                               width=self.keysize,
                               command=lambda k=k: self._attach_key_press(k)).grid(row=0, column=i)
                    i += 1
            elif row == 'row2':
                i = 2
                for k in self.keyStyle[row]:
                    if k == 'Bksp':
                        ttk.Button(self.row2,
                                   style="vKeyboardSpecial.TButton",
                                   text=k,
                                   width=self.keysize * 2,
                                   command=lambda k=k: self._attach_key_press(k)).grid(row=0, column=i)
                    elif k == 'BACK':
                        ttk.Button(self.row2,
                                   style="vKeyboardSpecial.TButton",
                                   text=k,
                                   width=self.keysize * 2,
                                   command=lambda k=k: self._attach_key_press(k)).grid(row=0, column=i)
                    elif k == 'ENTER':
                        ttk.Button(self.row2,
                                   style="vKeyboardSpecial.TButton",
                                   text=k,
                                   width=self.keysize * 2.5,
                                   command=lambda k=k: self._attach_key_press(k)).grid(row=0, column=i)
                    else:
                        ttk.Button(self.row2,
                                   style="vKeyboard.TButton",
                                   text=k,
                                   width=self.keysize,
                                   command=lambda k=k: self._attach_key_press(k)).grid(row=0, column=i)
                    i += 1


    def _attach_key_press(self, k):
        if k == '>>>':
            self.attach.tk_focusNext().focus_set()
        elif k == '<<<':
            self.attach.tk_focusPrev().focus_set()
        elif k == 'Sym':
            self.Symbol_Frame.tkraise()
        elif k == 'abc':
            self.alpha_Frame.tkraise()
        elif k == 'ABC':
            self.Alpha_Frame.tkraise()
        elif k == 'Bksp':
            self.remaining = self.attach.get()[:-1]
            self.attach.delete(0, END)
            self.attach.insert(0, self.remaining)
        elif k == 'ENTER':
            print('Host_box.Enter_click')
            t1 = self.parentPage.get_entry()
            u1 = t1.get()
            with open('./data/host.conf', 'wb') as pfile:
                pfile.write("%s" % u1)
            self.parentPage.destroy()
            Host_box.object.grab_release()
            Host_box.object.destroy()

        elif k == 'BACK':
            self.parentPage.destroy()
            Host_box.object.grab_release()
            Host_box.object.destroy()
        elif k == '[ space ]':
            self.attach.insert(END, ' ')
        else:
            self.attach.insert(END, k)
