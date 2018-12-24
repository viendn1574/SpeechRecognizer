# -*- coding: utf-8 -*-
import mmap
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
import Host_box
from gtts import gTTS
import RPi.GPIO as GPIO

feature_support.login = False
feature_support.add=0

def List_click():
    print('feature_support.List_click')
    list_box_gui= Toplevel()
    list_box_gui.grab_set()
    list_box_gui.resizable(False,False)
    list_box_gui.geometry("400x230+200+80")
    bAdd= Button(list_box_gui, text="Add",width=10,command=lambda: Management.Add_click(list_box_gui))
    bAdd.place(relx=0.05, rely=0.05)
    bEdit=Button(list_box_gui, text="Edit",width=10,command=lambda: Management.Edit_click(list_box_gui,Lb))
    bEdit.place(relx=0.37, rely=0.05)
    bDel=Button(list_box_gui,text="Delete",width=10,command=lambda: Management.Delete_click(list_box_gui,Lb))
    bDel.place(relx=0.67, rely=0.05)
    Lb=Listbox(list_box_gui,width=44)
    Lb.place(relx=0.05, rely=0.2)
    with open('./data/list_person.txt','rb') as lpfile:
        for person in lpfile:
            row=person.split()
            if (row != []):
                Lb.insert(END,"%s ----- %s"%(row[0],row[1]) )
    list_box_gui.mainloop()
    sys.stdout.flush()


rec= Module_recoder.Recorder(channels=1,frames_per_buffer=1024)
global recfile2


def Record_click(event,label1):
    GPIO.remove_event_detect(18)
    GPIO.add_event_detect(18, GPIO.RISING, callback=lambda event, Label1=label1: feature_support.Record_release(event,Label1), bouncetime=1200)
    if os.path.exists('nonblocking.wav'):
        os.remove('nonblocking.wav')
    if os.path.exists('nonblocking_filtered.wav'):
        os.remove('nonblocking_filtered.wav')
    global recfile2
    global rec
    recfile2= rec.open('nonblocking.wav', 'wb')
    print('feature_support.Record_click')
    if feature_support.add > 0:
        if feature_support.add < 9:
            label1.configure(text="Thêm lần thứ %d" %feature_support.add)

        else:
            label1.configure(text="Thêm lần cuối cùng")

    if feature_support.add == 0:
        label1.configure(text="")

    recfile2.start_recording()
    sys.stdout.flush()

data1 =[]

def Record_release(event,Label1):
    print('feature_support.Record_release')
    GPIO.remove_event_detect(18)
    GPIO.add_event_detect(18, GPIO.FALLING, callback=lambda event, Label1=Label1:  feature_support.Record_click(event,Label1), bouncetime=1200)
    global recfile2
    recfile2.stop_recording()
    recfile2.close()
    global data1
    if feature_support.add==0:
        features=extract_features.extract_features('nonblocking.wav')
        result=NeuralNetwork.compute(features)

        print(result)
        if result >= 1:
            name= getNamePerson(int(result))
            Label1.configure(text="Xin chào %s"%name)
            os.system("mpg123 ./data/%s.mp3"%name)
            GPIO.output(23, 0)


        if result == 0:
            Label1.configure(text="Xin thử lại")
            os.system("mpg123 ./data/xinthulai.mp3")

        if result == -1:
            Label1.configure(text="Bạn nói nhanh quá")
            os.system("mpg123 ./data/bannoinhanhqua.mp3")



    if feature_support.add > 0:
        features=extract_features.extract_features('nonblocking.wav')
        if len(features)>0:
            data1.extend(features)
            Label1.configure(text="Thêm thành công lần %d" %feature_support.add)
            feature_support.add +=1
        else:
            Label1.configure(text="Thêm không thành công lần %d, bạn nói nhanh quá." %feature_support.add)
    if feature_support.add==9:
        number_person=0
        with open('./data/list_person.txt','a') as lpfile:
            with open('person_temp.txt','r') as ptemp:
                person=ptemp.readline()
                lpfile.write(person+'\n')
                number_person=person[0]
                tts = gTTS(text=("Xin chào %s"%person.split()[1]).decode('utf-8'), lang='vi')
                tts.save("./data/%s.mp3"%person.split()[1].decode('utf-8'))
                ptemp.close()
            lpfile.close()
        for i in range(0,len(data1)):
            data1[i]=(numpy.append([1],data1[i])).tolist()
        NeuralNetwork.add_model(data1,number_person)
        data1 = []
        feature_support.add = 0
        Label1.configure(text="")
        os.remove('person_temp.txt')
        GUI_Builder.object.Button1.config(state=DISABLED)

    #os.remove('nonblocking.wav')
    #os.remove('nonblocking_filtered.wav')
    sys.stdout.flush()


def CancleAdd_click():
    GUI_Builder.object.Label1.configure(text="Add cancle")
    feature_support.add=0
    global data1
    data1=[]
    GUI_Builder.object.Button1.config(state=DISABLED)
    os.remove('person_temp.txt')

def Login_click(buttonLogin,buttonList):
    print('feature_support.Login_click')
    if feature_support.login == False:
        Login_box.GUI()
    else:
        feature_support.login = False
        buttonLogin.configure(text="Log in")
        buttonList.config(state=DISABLED)
        GUI_Builder.object.ButtonConfig.config(state=DISABLED)
        if feature_support.add>0:
            feature_support.CancleAdd_click()

def getNamePerson(index):
    with open('./data/list_person.txt','r') as lpfile:
        list_person=lpfile.readlines()
        person=list_person[index-1]
        name=person.split()
        return " ".join(name[item] for item in range(1,name.__len__()))

def Setting_click():
    print('feature_support.Setting_click')
    Host_box.GUI()
