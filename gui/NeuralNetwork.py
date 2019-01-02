import requests
import numpy
import json
from pybrain.tools.xml import NetworkReader
import os
import psutil
process = psutil.Process(os.getpid())
model = []
seed = 7
numpy.random.seed(seed)
def init_model():
    global model
    with open('./data/list_person.txt','r') as lpfile:
        row_count = sum(1 for row in lpfile)
    for i in range(1,row_count+1):
        net = NetworkReader.readFrom('./model/net%d.xml'%i)
        model.insert(model.__len__(),net)


def add_model(dataset,number_person):
    json_data = json.dumps(dataset)
    with open('./data/host.conf','r') as ptemp:
        person=ptemp.readline()
    response = requests.post('http://%s:8000' % person, data=json_data)
    with open('./model/net%d.xml'%int(number_person), 'wb') as file:
        file.write(response.content)
    net = NetworkReader.readFrom('./model/net%d.xml'%int(number_person))
    model.insert(model.__len__(),net)

def compute(a):
    print ('compute')
    print(process.memory_info().rss)
    global model
    number_person=model.__len__()
    if number_person==0:
        return 0
    if len(a) <= 20 :
        print ('compute')
        print(process.memory_info().rss)
        return -1
    result_allperson=list(numpy.zeros(number_person))
    for person_count in range(0,number_person):
        result_person=list(numpy.zeros(2))
        for i in range(0,len(a)):
            activate=list(model[person_count].activate(a[i]))
            if activate[1] >= 0.5:
                result_person[1] += 1
            else: result_person[0] += 1
            print activate
        #print result_person
        print result_person[1]/len(a)
        if result_person[1]/len(a) >= 0.7:
            result_allperson[person_count]=result_person[1]/len(a)
    print result_allperson
    if max(result_allperson) >= 0.7:
        print ('compute end')
        print(process.memory_info().rss)
        return result_allperson.index(max(result_allperson))+1
    else:
        print ('compute end')
        print(process.memory_info().rss)
        return 0


def remove_model(indexModel):
    global model
    del model[indexModel-1]