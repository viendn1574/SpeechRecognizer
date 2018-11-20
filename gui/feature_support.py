# -*- coding: utf-8 -*-
import csv
import mmap
from time import sleep

import numpy
import os

import pygame
from pygame import mixer

import NeuralNetwork
from Tkinter import *
import Login_box
import Module_recoder
import extract_features
import feature_support
import Management
import GUI_Builder
from gtts import gTTS

feature_support.login = False
feature_support.add=0

def List_click():
    print('feature_support.List_click')
    list_box_gui= Toplevel()
    list_box_gui.grab_set()
    list_box_gui.resizable(False,False)
    list_box_gui.geometry("300x250+700+200")
    bAdd= Button(list_box_gui, text="Add",width=10,command=lambda: Management.Add_click(list_box_gui))
    bAdd.place(relx=0.05, rely=0.05)
    bEdit=Button(list_box_gui, text="Edit",width=10,command=lambda: Management.Edit_click(list_box_gui,Lb))
    bEdit.place(relx=0.375, rely=0.05)
    bDel=Button(list_box_gui,text="Delete",width=10,command=lambda: Management.Delete_click(list_box_gui,Lb))
    bDel.place(relx=0.7, rely=0.05)
    Lb=Listbox(list_box_gui,width=45)
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
    active = pygame.mixer.get_init()
    if active != None:
        pygame.mixer.music.stop()
        pygame.mixer.quit()
        pygame.quit()
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
    global recfile2
    recfile2.stop_recording()
    recfile2.close()
    global data1
    pygame.init()
    if feature_support.add==0:
        features=extract_features.extract_features('nonblocking.wav')
        result=NeuralNetwork.compute(features)

        print(result)
        if result >= 1:
            name= getNamePerson(int(result))
            Label1.configure(text="Xin chào %s"%name)
            active = pygame.mixer.get_init()
            if active == None:
                pygame.init()
            with open("./data/%s.mp3"%name.decode('utf-8')) as f:
                m = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
                pygame.mixer.music.load(m)
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy():
                    pygame.time.Clock().tick(10)
                m.close()


        if result == 0:
            Label1.configure(text="Xin thử lại")

            mixer.music.load("./data/xinthulai.mp3")
            mixer.music.play()

        if result == -1:
            Label1.configure(text="Bạn nói nhanh quá")

            mixer.music.load("./data/bannoinhanhqua.mp3")
            mixer.music.play()



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
        if feature_support.add>0:
            feature_support.CancleAdd_click()

def getNamePerson(index):
    with open('./data/list_person.txt','r') as lpfile:
        list_person=lpfile.readlines()
        person=list_person[index-1]
        name=person.split()
        return " ".join(name[item] for item in range(1,name.__len__()))
