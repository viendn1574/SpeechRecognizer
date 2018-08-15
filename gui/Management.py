import fileinput
import os
import tkMessageBox
from Tkinter import Toplevel, Label, Entry, Button, ACTIVE, END, NORMAL

import NeuralNetwork
import feature_support
import GUI_Builder


def Add_click(root):
    root.grab_release()
    print("add click")
    popup= Toplevel()
    popup.resizable(False,False)
    popup.geometry("200x150+700+300")
    popup.grab_set()
    def Cancle():
        popup.grab_release()
        root.grab_set()
        popup.destroy()


    def OK(t1):
        print('feature_support.OK_click')
        u1 = t1.get()
        with open('./data/list_person.txt','r') as lpfile:
            person_count = sum(1 for person in lpfile)
            with open('person_temp.txt','w') as pfile:
                pfile.write("%s %s"%(person_count+1,u1))
                pfile.close()
            lpfile.close()
        GUI_Builder.top.Button1.config(state=NORMAL)
        popup.destroy()
        root.destroy()
        feature_support.add += 1

    popup.wm_title("Enter name")
    l1 = Label(popup, text="Name")

    t1 = Entry(popup, textvariable="")

    b1 = Button(popup, text="OK",width=7, command= lambda: OK(t1))
    b2 = Button(popup, text="Cancle",width=7, command=Cancle)
    l1.pack()
    t1.pack()
    b1.place(relx=0.18, rely=0.6)
    b2.place(relx=0.52, rely=0.6)

def Edit_click(root,Listbox):
    if (Listbox.curselection()!=()):
        root.grab_release()
        print("edit click")
        popup= Toplevel()
        popup.resizable(False,False)
        popup.geometry("200x150+700+300")
        popup.grab_set()
        def Cancle():
            popup.grab_release()
            root.grab_set()
            popup.destroy()


        def OK(t1,Listbox):
            print('feature_support.OK_click')
            u1 = t1.get()
            newrow=[]
            selected=Listbox.get(ACTIVE)
            with open('./data/list_person.txt','r') as lpfile:
                for person in lpfile:
                    row=person.split()
                    if (row!=[]):
                        if (int(row[0])==int(selected[0])):
                            row[1]=u1
                        newrow.append(row)
            with open('./data/list_person.txt','w') as lpfile:
                i=0
                for row in newrow:
                    Listbox.delete(i)
                    Listbox.insert(i,"%d ----- %s"%(int(row[0]),row[1]) )
                    lpfile.write(row)
                    i += 1
            Listbox.update()
            popup.destroy()
            root.grab_set()
        popup.wm_title("Enter name")
        l1 = Label(popup, text="Name")

        t1 = Entry(popup, textvariable="")

        b1 = Button(popup, text="OK",width=7, command= lambda: OK(t1,Listbox))
        b2 = Button(popup, text="Cancle",width=7, command=Cancle)
        l1.pack()
        t1.pack()
        b1.place(relx=0.18, rely=0.6)
        b2.place(relx=0.52, rely=0.6)
        popup.mainloop()
    else:
        tkMessageBox.showinfo("Error", "Vui long chon doi tuong")

def Delete_click(root,Listbox):
    if (Listbox.curselection()!=()):
        root.grab_release()
        print("Delete click")
        popup= Toplevel()
        popup.resizable(False,False)
        popup.geometry("200x150+700+300")
        popup.grab_set()

        def Cancle():
            popup.grab_release()
            root.grab_set()
            popup.destroy()

        def OK(Listbox):
            print('feature_support.OK_click')

            newrow=[]
            selected=Listbox.get(ACTIVE)
            for line in fileinput.input("./data/database.csv", inplace=True):
                if line=='\n':
                    continue
                if int(line[0]) < int(selected[0]):
                    print line,
                if int(line[0]) > int(selected[0]):
                    newline=line.split()
                    newline[0]=str(int(newline[0])-1)
                    print " ".join(newline)
                    print '\n',
            fileinput.close()
            with open('./data/list_person.txt','r') as lpfile:
                row_count = sum(1 for row in lpfile)
            os.remove('./model/net%d.xml'%int(selected[0]))
            if (row_count > 1)or(int(selected[0])!=row_count):
                for i in range(int(selected[0])+1,row_count+1):
                    os.rename('./model/net%d.xml'%i,'./model/net%d.xml'%(i-1))
            with open('./data/list_person.txt','r') as lpfile:
                for row in lpfile:
                    if (row!=[]):
                        row=row.split()
                        if (int(row[0])<int(selected[0])):
                            newrow.append(row)
                        if (int(row[0])>int(selected[0])):
                            row[0]=int(row[0])-1
                            newrow.append(row)
            Listbox.delete(0,END)
            with open('./data/list_person.txt','w') as lpfile:
                i=0
                for row in newrow:
                    Listbox.insert(i,"%d ----- %s" % (int(row[0]), row[1]))
                    lpfile.write("%s %s\n"%(row[0],row[1]))
                    i += 1
            NeuralNetwork.remove_model(int(selected[0]))
            popup.destroy()
            root.grab_set()

        popup.wm_title("Delete")
        l1 = Label(popup, text="Ban co muon xoa !")
        b1 = Button(popup, text="OK",width=7, command= lambda: OK(Listbox))
        b2 = Button(popup, text="Cancle",width=7, command=Cancle)
        l1.pack()
        b1.place(relx=0.18, rely=0.6)
        b2.place(relx=0.52, rely=0.6)
        popup.mainloop()
    else:
        tkMessageBox.showinfo("Error", "Vui long chon doi tuong")
