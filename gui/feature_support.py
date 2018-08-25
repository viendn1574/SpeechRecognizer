import csv
import numpy
import os
import NeuralNetwork
from Tkinter import *
import Login_box
import Module_recoder
import extract_features
import feature_support
import Management
import GUI_Builder
import Login

feature_support.add=0

def List_click():
    print('feature_support.List_click')
    root= Toplevel()
    root.grab_set()
    root.resizable(False,False)
    root.geometry("300x250+700+200")
    bAdd= Button(root, text="Add",width=10,command=lambda: Management.Add_click(root))
    bAdd.place(relx=0.05, rely=0.05)
    bEdit=Button(root, text="Edit",width=10,command=lambda: Management.Edit_click(root,Lb))
    bEdit.place(relx=0.375, rely=0.05)
    bDel=Button(root,text="Delete",width=10,command=lambda: Management.Delete_click(root,Lb))
    bDel.place(relx=0.7, rely=0.05)
    Lb=Listbox(root,width=45)
    Lb.place(relx=0.05, rely=0.2)
    with open('./data/list_person.txt','r') as lpfile:
        for person in lpfile:
            row=person.split()
            if (row != []):
                Lb.insert(END,"%d ----- %s"%(int(row[0]),row[1]) )
    root.mainloop()
    sys.stdout.flush()


rec = Module_recoder.Recorder(channels=1,frames_per_buffer=1024)
global recfile2


def Record_click(event,label1):

    if os.path.exists('nonblocking.wav'):
        os.remove('nonblocking.wav')
    if os.path.exists('nonblocking_filtered.wav'):
        os.remove('nonblocking_filtered.wav')
    global recfile2
    recfile2= rec.open('nonblocking.wav', 'wb')
    print('feature_support.Record_click')
    global add
    if add > 0:
        if add < 9:
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
            name= getNamePerson(int(result))
            Label1.configure(text="Xin chao %s"%name)
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
    if add==9:
        number_person=0
        with open('./data/list_person.txt','a') as lpfile:
            with open('person_temp.txt','r') as ptemp:
                person=ptemp.readline()
                lpfile.write(person+'\n')
                number_person=person[0]
                ptemp.close()
            lpfile.close()
        with open('./data/database.csv','a') as csvdata:
            writer =csv.writer(csvdata,delimiter=' ')
            for i in range(0,len(data1)):
                data1[i]=numpy.append([1],data1[i])
                a=list(data1[i])
                a[0]=int(number_person)
                writer.writerow(a,)
        NeuralNetwork.add_model(data1)
        data1 = []
        add = 0
        Label1.configure(text="")
        os.remove('person_temp.txt')
        GUI_Builder.top.Button1.config(state=DISABLED)

    os.remove('nonblocking.wav')
    os.remove('nonblocking_filtered.wav')
    sys.stdout.flush()


def CancleAdd_click():
    GUI_Builder.top.Label1.configure(text="Add cancle")
    global add
    add=0
    global data1
    data1=[]
    GUI_Builder.top.Button1.config(state=DISABLED)
    os.remove('person_temp.txt')

def Login_click(buttonLogin,buttonList):
    print('feature_support.Login_click')
    #Login_box.popuplogin(buttonLogin,buttonList)
    Login.GUI()
    sys.stdout.flush()

def init(top, gui, *args, **kwargs):
    global w, top_level, root
    w = gui
    top_level = top
    root = top

def getNamePerson(index):
    with open('./data/list_person.txt','r') as lpfile:
        list_person=lpfile.readlines()
        person=list_person[index-1]
        name=person.split()
        return name[1]
