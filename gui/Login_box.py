from Tkinter import *
import feature_support
import tkMessageBox


login = False

def popuplogin(buttonLogin, buttonList):
    global login
    if login == False:

        popup = Toplevel()
        popup.resizable(False,False)
        popup.geometry("200x150+700+300")

        def Cancle():
            popup.grab_release()
            popup.destroy()

        def OK(t1, t2,buttonLogin ,buttonList):
            print('feature_support.OK_click')
            u1 = t1.get()
            u2 = t2.get()
            if u1 == 'Admin' and u2 == 'admin':
                global login
                login = True
                buttonLogin.configure(text="Log out")
                buttonList.config(state=NORMAL)
                tkMessageBox.showinfo("Valid", "Log in Sucessfully")
                popup.grab_release()
                popup.destroy()

            elif u1 != 'Admin' or u2 != 'admin':
                tkMessageBox.showinfo("Invalid", "Wrong User or Password ,try again")
        popup.wm_title("Login")
        l1 = Label(popup, text="User")
        l2 = Label(popup, text="Password")
        t1 = Entry(popup, textvariable="")
        t2 = Entry(popup, show="*", textvariable="")
        b1 = Button(popup, text="OK", width=7, command= lambda: OK(t1, t2,buttonLogin, buttonList))
        b2 = Button(popup, text="Cancle",width=7, command=Cancle)
        l1.pack()
        t1.pack()
        l2.pack()
        t2.pack()
        b1.place(relx=0.18, rely=0.6)
        b2.place(relx=0.52, rely=0.6)
        popup.grab_set()

        popup.mainloop()
    else:
        login = False
        buttonLogin.configure(text="Log in")
        buttonList.config(state=DISABLED)
        if feature_support.add>0:
            feature_support.CancleAdd_click()







