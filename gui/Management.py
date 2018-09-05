# -*- coding: utf-8 -*-
import fileinput
import os
import tkMessageBox
from Tkinter import Toplevel, Label, Entry, Button, ACTIVE, END, NORMAL
import NeuralNetwork
import Add_box
import Edit_box


def Add_click(root):
    Add_box.GUI(root)

def Edit_click(root,Listbox):
    if (Listbox.curselection()!=()):
        root.grab_release()
        Edit_box.GUI(root, Listbox)

    else:
        tkMessageBox.showinfo("Error", "Vui lòng chọn đối tượng")

def Delete_click(root,Listbox):
    if (Listbox.curselection()!=()):
        root.grab_release()
        print("Delete click")
        popup= Toplevel()
        popup.resizable(False,False)
        popup.geometry("200x100+700+300")
        popup.grab_set()

        def Cancle():
            popup.grab_release()
            root.grab_set()
            popup.destroy()

        def OK(Listbox):
            print('feature_support.OK_click')

            newrow=[]
            selected=Listbox.get(ACTIVE)
            os.remove("./data/%s.mp3"%selected.split(' ----- ')[1])
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
            with open('./data/list_person.txt','rb') as lpfile:
                row_count = sum(1 for row in lpfile)
            os.remove('./model/net%d.xml'%int(selected[0]))
            if (row_count > 1)or(int(selected[0])!=row_count):
                for i in range(int(selected[0])+1,row_count+1):
                    os.rename('./model/net%d.xml'%i,'./model/net%d.xml'%(i-1))
            with open('./data/list_person.txt','rb') as lpfile:
                for row in lpfile:
                    if (row!=[]):
                        row=row.split()
                        if (int(row[0])<int(selected[0])):
                            newrow.append(row)
                        if (int(row[0])>int(selected[0])):
                            row[0]=int(row[0])-1
                            newrow.append(row)
            Listbox.delete(0,END)
            with open('./data/list_person.txt','wb') as lpfile:
                i=0
                for row in newrow:
                    Listbox.insert(i,"%d ----- %s" % (int(row[0]), row[1]))
                    lpfile.write("%s %s\n"%(row[0],row[1]))
                    i += 1
            NeuralNetwork.remove_model(int(selected[0]))
            popup.destroy()
            root.grab_set()

        popup.wm_title("Delete")
        l1 = Label(popup, text="Bạn có muốn xóa !")
        b1 = Button(popup, text="OK",width=7, command= lambda: OK(Listbox))
        b2 = Button(popup, text="Cancle",width=7, command=Cancle)
        l1.place(relx=0.25, rely=0.2)
        b1.place(relx=0.18, rely=0.6)
        b2.place(relx=0.52, rely=0.6)
        popup.mainloop()
    else:
        tkMessageBox.showinfo("Error", "Vui lòng chọn đối tượng")
