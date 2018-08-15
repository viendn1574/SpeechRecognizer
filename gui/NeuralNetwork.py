import csv
import numpy
import pandas

from pybrain.tools.shortcuts import buildNetwork
from pybrain.datasets import ClassificationDataSet
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.structure.modules   import SoftmaxLayer
from pybrain.tools.xml import NetworkWriter
from pybrain.tools.xml import NetworkReader

model = []

def init_model():
    global model
    with open('./data/list_person.txt','r') as lpfile:
        row_count = sum(1 for row in lpfile)
    for i in range(1,row_count+1):
        net = NetworkReader.readFrom('./model/net%d.xml'%i)
        model.insert(model.__len__(),net)


def add_model(dataset):
    ds = ClassificationDataSet(117,1,nb_classes=2)
    dataframe = pandas.read_csv("./data/train.csv", delimiter=" ",header=None)
    data_train = dataframe.values
    #dataframe = pandas.read_csv("database.csv", delimiter=" ", header=None)
    data_train=numpy.concatenate((data_train,dataset))
    input=data_train[:,1:118].astype(float)
    target=data_train[:,0]
    target = numpy.reshape(target, (-1, 1))
    ds.setField('input', input)
    ds.setField('target', target)
    ds._convertToOneOfMany()
    net = buildNetwork(ds.indim, 50, ds.outdim, outclass=SoftmaxLayer)
    def train():
        global model
        back=BackpropTrainer(net,ds,learningrate = 0.0001, momentum = 0.1,verbose=True, weightdecay=0.1)
        #back.trainUntilConvergence(verbose=True)
        back.trainEpochs(100)
        NetworkWriter.writeToFile(net, './model/net%d.xml'%(model.__len__()+1))
        model.append(net)
    train()

def compute(a):
    global model
    number_person=model.__len__()
    if number_person==0:
        return 0
    if len(a) <= 20 :
        return -1
    result_allperson=list(numpy.zeros(number_person))
    for person_count in range(0,number_person):
        result_person=list(numpy.zeros(2))
        for i in range(0,len(a)):
            activate=list(model[person_count].activate(a[i]))
            if activate[1] >= 0.7:
                result_person[1] += 1
            else: result_person[0] += 1
        print result_person
        print result_person[1]/len(a)
        if result_person[1]/len(a) >= 0.8:
            result_allperson[person_count]=result_person[1]/len(a)
    print result_allperson
    if max(result_allperson) >= 0.8:
        return result_allperson.index(max(result_allperson))+1
    else: return 0


def remove_model(indexModel):
    global model
    del model[indexModel-1]