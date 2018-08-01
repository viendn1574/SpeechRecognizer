import tkMessageBox

import librosa
import csv
import numpy
import os

from sklearn import decomposition

import NeuralNetwork

from Tkinter import *


import Login_box
import Module_recoder
import extract_features

add=0

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
        with open('list_person.txt','r') as lpfile:
            person_count = sum(1 for person in lpfile)
            with open('person_temp.txt','w') as pfile:
                pfile.write("%s %s"%(person_count+1,u1))
                pfile.close()
            lpfile.close()

        popup.destroy()
        root.destroy()
        global add
        add += 1

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
            with open('list_person.txt','r') as lpfile:
                list_person=lpfile.read()
                for person in list_person:
                    row=person.split()
                    if (row!=[]):
                        if (int(row[0])==int(selected[0])):
                            row[1]=u1
                        newrow.append(row)
            with open('list_person.txt','w') as lpfile:
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

def List_click():
    print('feature_support.List_click')
    root= Toplevel()
    root.grab_set()
    root.resizable(False,False)
    root.geometry("300x250+700+200")
    bAdd= Button(root, text="Add",width=10,command=lambda: Add_click(root))
    bAdd.place(relx=0.05, rely=0.05)
    bEdit=Button(root, text="Edit",width=10,command=lambda: Edit_click(root,Lb))
    bEdit.place(relx=0.375, rely=0.05)
    bDel=Button(root,text="Delete",width=10)
    bDel.place(relx=0.7, rely=0.05)
    Lb=Listbox(root,width=45)
    Lb.place(relx=0.05, rely=0.2)
    with open('list_person.txt','r') as lpfile:
        for person in lpfile:
            row=person.split()
            if (row != []):
                Lb.insert(END,"%d ----- %s"%(int(row[0]),row[1]) )
    root.mainloop()
    sys.stdout.flush()


rec = Module_recoder.Recorder(channels=1)
global recfile2


def Record_click(event,label1):
    if os.path.exists('nonblocking.wav'):
        os.remove('nonblocking.wav')
    global recfile2
    recfile2= rec.open('nonblocking.wav', 'wb')
    print('feature_support.Record_click')
    global add
    if add > 0:
        if add < 11:
            label1.configure(text="Add lan thu %d" %add)

        else:
            label1.configure(text="Add lan cuoi")

    if add == 0:
        label1.configure(text="")

    recfile2.start_recording()
    sys.stdout.flush()

data1 =[]

def Record_release(event,Label1):
    print('feature_support.Record_release')
    global recfile2
    recfile2.stop_recording()
    recfile2.close()
    global add
    global data1
    if add==0:
        features=extract_features.extract_features('nonblocking.wav')
        result=NeuralNetwork.compute(features)

        print(result)
        if result >= 1:
            Label1.configure(text="%s"%result)
        if result == 0:
            Label1.configure(text="Xin thu lai")
        if result == -1:
            Label1.configure(text="Ban noi nhanh qua")
    if add > 0:
        features=extract_features.extract_features('nonblocking.wav')
        if len(features)>0:
            data1.extend(features)
            Label1.configure(text="Add thanh cong lan %d" %add)
            add +=1
        else:
            Label1.configure(text="Add khong thanh cong lan %d, ban noi qua nhanh" %add)
    if add==11:
        number_person=0
        with open('list_person.txt','a') as lpfile:
            with open('person_temp.txt','r') as ptemp:
                person=ptemp.readline()
                lpfile.write(person+'\n')
                number_person=person[0]
                ptemp.close()
            lpfile.close()
        with open('database.csv','a') as csvdata:
            writer =csv.writer(csvdata,delimiter=' ')
            for i in range(0,len(data1)):
                a=numpy.append([int(number_person)],data1[i])
                writer.writerow(a,)
        data1 = []
        add = 0
        Label1.configure(text="")
        os.remove('person_temp.txt')
        NeuralNetwork.init_dataset()

    os.remove('nonblocking.wav')
    sys.stdout.flush()


def CancleAdd_click(Label1):
    Label1.configure(text="Add cancle")
    global add
    add=0
    global data1
    for i in range(0,5):
        data1[i]=[]
    os.remove('datatemp.csv')

def Login_click(button):
    print('feature_support.Login_click')
    Login_box.popuplogin(button)
    sys.stdout.flush()

def init(top, gui, *args, **kwargs):
    global w, top_level, root
    w = gui
    top_level = top
    root = top


def destroy_window():
    # Function which closes the window.
    global top_level
    top_level.destroy()
    top_level = None




