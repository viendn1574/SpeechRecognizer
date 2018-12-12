import ttk
from Tkinter import *
import tkMessageBox
import GUI_Builder
import Login_box
import feature_support


# -- Declaration of font styles --- #
font_title = ("Helvetica", 18, "bold")
font_message = ("Helvetica", 14)
font_message_small = ("Helvetica", 11)
font_vKeyboard = ("Helvetica", 10)
font_vKeyboardSpecialKeys = ("Helvetica", 10, "bold")

# -- GUI's main class -- #
Login_box.object=None
class GUI(Toplevel):
    def __init__(self, *args, **kwargs):
        Toplevel.__init__(self, *args, **kwargs)

        container = ttk.Frame(self, width=480, height=320)
        container.grid_propagate(0)
        container.pack(fill="both", expand=1)

        ttk.Style().configure("vKeyboard.TButton", font=font_vKeyboard)
        ttk.Style().configure("vKeyboardSpecial.TButton", font=font_vKeyboardSpecialKeys)

        self.frames = {}

        F=LoginPage
        page_name = F.__name__
        frame = F(parent=container)
        self.frames[page_name] = frame

        frame.grid(row=0, column=0, sticky="nsew")
        self.geometry("%dx%d+%d+%d"%(480,320,0,0))
        self.showFrame("LoginPage")
        Login_box.object=self
        self.grab_set()

    def showFrame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

class LoginPage(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)
        label1 = ttk.Label(self, text="Login Page", font=font_title)
        label1.pack(side="top", fill="x", pady=7, padx=10)

        self.label1 = ttk.Label(self, text="User name:", font=font_message)
        self.label1.pack(side="top")
        self.entry1 = ttk.Entry(self)
        self.entry1.pack(side="top")

        self.label0 = ttk.Label(self, text="  ", font=font_message)
        self.label0.pack(side="top")
        self.label2 = ttk.Label(self, text="Password:", font=font_message)
        self.label2.pack(side="top")
        self.entry2 = ttk.Entry(self, show="*")
        self.entry2.pack(side="top")

        self.frame1 = ttk.Frame(self, width=480, height=320)
        self.frame1.pack(side="top", pady=30,padx=15)

        self.keysize = 4

        self.entry1.bind("<FocusIn>", lambda e:  self.show_vKeyboard(1))
        self.entry2.bind("<FocusIn>", lambda e:  self.show_vKeyboard(2))

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

            self.frame1 = ttk.Frame(self, width=480, height=320)
            self.frame1.pack(side="top", pady=30,padx=15)
            self.kb = vKeyboard( parentPage = self,
                                 attach=self.entry1,
                                 x=self.entry1.winfo_rootx(),
                                 y=self.entry1.winfo_rooty() + self.entry1.winfo_reqheight(),
                                 keysize=self.keysize,
                                 parent=self.frame1)

        elif k == 2:
            self.frame1.destroy()
            self.kb.destroy()

            self.frame1 = ttk.Frame(self, width=480, height=320)
            self.frame1.pack(side="top", pady=30,padx=15)
            self.kb = vKeyboard( parentPage = self,
                                 attach=self.entry2,
                                 x=self.entry2.winfo_rootx(),
                                 y=self.entry2.winfo_rooty() + self.entry2.winfo_reqheight(),
                                 keysize=self.keysize,
                                 parent=self.frame1)

    def get_entry(self):
        return self.entry1, self.entry2

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

        # --- Uppercase alphabet sub-keyboard --- #
        self.Alpha_Frame = ttk.Frame(parent)
        self.Alpha_Frame.grid(row=0, column=0, sticky="nsew")

        self.row1_Alpha = ttk.Frame(self.Alpha_Frame)
        self.row2_Alpha = ttk.Frame(self.Alpha_Frame)
        self.row3_Alpha = ttk.Frame(self.Alpha_Frame)
        self.row4_Alpha = ttk.Frame(self.Alpha_Frame)

        self.row1_Alpha.grid(row=1)
        self.row2_Alpha.grid(row=2)
        self.row3_Alpha.grid(row=3)
        self.row4_Alpha.grid(row=4)

        # --- Symbols and numerals sub-keyboard --- #
        self.Symbol_Frame = ttk.Frame(parent)
        self.Symbol_Frame.grid(row=0, column=0, sticky="nsew")

        self.row1_Symbol = ttk.Frame(self.Symbol_Frame)
        self.row2_Symbol = ttk.Frame(self.Symbol_Frame)
        self.row3_Symbol = ttk.Frame(self.Symbol_Frame)
        self.row4_Symbol = ttk.Frame(self.Symbol_Frame)

        self.row1_Symbol.grid(row=1)
        self.row2_Symbol.grid(row=2)
        self.row3_Symbol.grid(row=3)
        self.row4_Symbol.grid(row=4)

        # --- Initialize all sub-keyboards --- #
        self.keyState = 1
        self.init_keys()

        self.alpha_Frame.tkraise()

        self.pack()

    def init_keys(self):
        self.alpha = {
            'row1': ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'Bksp'],
            'row2': ['Sym', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l'],
            'row3': ['ABC', 'z', 'x', 'c', 'v', 'b', 'n', 'm', 'ENTER'],
            'row4': ['<<<', '[ space ]', '>>>', 'BACK']
        }
        self.Alpha = {
            'row1': ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', 'Bksp'],
            'row2': ['Sym', 'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'],
            'row3': ['abc', 'Z', 'X', 'C', 'V', 'B', 'N', 'M', 'ENTER'],
            'row4': ['<<<', '[ space ]', '>>>', 'BACK']
        }
        self.Symbol = {
            'row1': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'Bksp'],
            'row2': ['abc', '!', '"', '$', '%', '&', '/', '(', ')', '[', ']', '='],
            'row3': ['@', '-', '_', '?', '#', '*', '{', '}', ':', ';', 'ENTER'],
            'row4': ['<<<','+', '[ space ]', '.', ',', '>>>', 'BACK']
        }

        for i in range(1, 4):
            if i == 1:
                self.keyStyle = self.alpha
                self.row1 = self.row1_alpha
                self.row2 = self.row2_alpha
                self.row3 = self.row3_alpha
                self.row4 = self.row4_alpha
            elif i == 2:
                self.keyStyle = self.Alpha
                self.row1 = self.row1_Alpha
                self.row2 = self.row2_Alpha
                self.row3 = self.row3_Alpha
                self.row4 = self.row4_Alpha
            elif i == 3:
                self.keyStyle = self.Symbol
                self.row1 = self.row1_Symbol
                self.row2 = self.row2_Symbol
                self.row3 = self.row3_Symbol
                self.row4 = self.row4_Symbol

            for row in self.keyStyle.iterkeys():  # iterate over dictionary of rows
                if row == 'row1':  # TO-DO: re-write this method
                    i = 1  # for readability and functionality
                    for k in self.keyStyle[row]:
                        if k == 'Bksp':
                            ttk.Button(self.row1,
                                       style="vKeyboardSpecial.TButton",
                                       text=k,
                                       width=self.keysize * 2,
                                       command=lambda k=k: self._attach_key_press(k)).grid(row=0, column=i)
                        else:
                            ttk.Button(self.row1,
                                       style="vKeyboard.TButton",
                                       text=k,
                                       width=self.keysize,
                                       command=lambda k=k: self._attach_key_press(k)).grid(row=0, column=i)
                        i += 1
                elif row == 'row2':
                    i = 2
                    for k in self.keyStyle[row]:
                        if k == 'Sym':
                            ttk.Button(self.row2,
                                       style="vKeyboardSpecial.TButton",
                                       text=k,
                                       width=self.keysize * 1.5,
                                       command=lambda k=k: self._attach_key_press(k)).grid(row=0, column=i)
                        elif k == 'abc':
                            ttk.Button(self.row2,
                                       style="vKeyboardSpecial.TButton",
                                       text=k,
                                       width=self.keysize * 1.5,
                                       command=lambda k=k: self._attach_key_press(k)).grid(row=0, column=i)
                        else:
                            ttk.Button(self.row2,
                                       style="vKeyboard.TButton",
                                       text=k,
                                       width=self.keysize,
                                       command=lambda k=k: self._attach_key_press(k)).grid(row=0, column=i)
                        i += 1
                elif row == 'row3':
                    i = 2
                    for k in self.keyStyle[row]:
                        if k == 'ABC':
                            ttk.Button(self.row3,
                                       style="vKeyboardSpecial.TButton",
                                       text=k,
                                       width=self.keysize * 1.5,
                                       command=lambda k=k: self._attach_key_press(k)).grid(row=0, column=i)
                        elif k == 'abc':
                            ttk.Button(self.row3,
                                       style="vKeyboardSpecial.TButton",
                                       text=k,
                                       width=self.keysize * 1.5,
                                       command=lambda k=k: self._attach_key_press(k)).grid(row=0, column=i)
                        elif k == 'ENTER':
                            ttk.Button(self.row3,
                                       style="vKeyboardSpecial.TButton",
                                       text=k,
                                       width=self.keysize * 2.5,
                                       command=lambda k=k: self._attach_key_press(k)).grid(row=0, column=i)
                        else:
                            ttk.Button(self.row3,
                                       style="vKeyboard.TButton",
                                       text=k,
                                       width=self.keysize,
                                       command=lambda k=k: self._attach_key_press(k)).grid(row=0, column=i)
                        i += 1
                else:
                    i = 3
                    for k in self.keyStyle[row]:
                        if k == '[ space ]':
                            ttk.Button(self.row4,
                                       style="vKeyboard.TButton",
                                       text='     ',
                                       width=self.keysize * 6,
                                       command=lambda k=k: self._attach_key_press(k)).grid(row=0, column=i)
                        elif k == 'BACK':
                            ttk.Button(self.row4,
                                       style="vKeyboardSpecial.TButton",
                                       text=k,
                                       width=self.keysize * 2,
                                       command=lambda k=k: self._attach_key_press(k)).grid(row=0, column=i)
                        else:
                            ttk.Button(self.row4,
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
            t1,t2 = self.parentPage.get_entry()
            u1 = t1.get()
            u2 = t2.get()

            print('feature_support.Enter_click')
            if u1 == '1' and u2 == '1':
                GUI_Builder.object.Button3.configure(text="Log out")
                GUI_Builder.object.Button4.config(state=NORMAL)
                GUI_Builder.object.ButtonConfig.config(state=NORMAL)
                tkMessageBox.showinfo("Valid", "Log in Sucessfully")
                feature_support.login=True
                self.parentPage.destroy()
                Login_box.object.grab_release()
                Login_box.object.destroy()
            elif u1 != '1' or u2 != '1':
                tkMessageBox.showinfo("Invalid", "Wrong User or Password ,try again")

        elif k == 'BACK':
            self.parentPage.destroy()
            Login_box.object.grab_release()
            Login_box.object.destroy()
        elif k == '[ space ]':
            self.attach.insert(END, ' ')
        else:
            self.attach.insert(END, k)
