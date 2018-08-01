try:
    from Tkinter import *
except ImportError:
    from Tkinter import *
import tkMessageBox

try:
    import ttk
    py3 = False
except ImportError:
    import tkinter.ttk as ttk
    py3 = True

import wave


def popuplogin(button):
    popup= Toplevel()
    popup.resizable(False,False)
    popup.geometry("200x150+700+300")

    def Cancle():
        popup.grab_release()
        popup.destroy()

    def OK(t1, t2,button):
        print('feature_support.OK_click')
        u1 = t1.get()
        u2 = t2.get()
        if u1 == 'Admin' and u2 == 'admin':
            tkMessageBox.showinfo("Valid", "Log in Sucessfully")
            button.config(state=NORMAL)
            popup.grab_release()
            popup.destroy()

        elif u1 != 'Admin' or u2 != 'admin':
            tkMessageBox.showinfo("Invalid", "Wrong User or Password ,try again")
    popup.wm_title("Login")
    l1 = Label(popup, text="User")
    l2 = Label(popup, text="Password")
    t1 = Entry(popup, textvariable="")
    t2 = Entry(popup, show="*", textvariable="")
    b1 = Button(popup, text="OK",width=7, command= lambda: OK(t1,t2,button))
    b2 = Button(popup, text="Cancle",width=7, command=Cancle)
    l1.pack()
    t1.pack()
    l2.pack()
    t2.pack()
    b1.place(relx=0.18, rely=0.6)
    b2.place(relx=0.52, rely=0.6)
    popup.grab_set()

    popup.mainloop()







