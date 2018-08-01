import csv
import numpy
import pandas

from pybrain.tools.shortcuts import buildNetwork
from pybrain.datasets import ClassificationDataSet
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.structure.modules   import SoftmaxLayer
from pybrain.tools.xml import NetworkWriter
from pybrain.tools.xml import NetworkReader

global net

def init_NeuralNetwork():
    global net
    net = NetworkReader.readFrom('net.xml')


def init_dataset():
    with open('list_person.txt','r') as lpfile:
        row_count = sum(1 for row in lpfile)
    ds = ClassificationDataSet(39,1,nb_classes=row_count+1)

    dataframe = pandas.read_csv("train.csv", delimiter=" ",header=None)
    dataset = dataframe.values
    dataframe = pandas.read_csv("database.csv", delimiter=" ", header=None)
    dataset=numpy.concatenate((dataset,dataframe.values))
    input=dataset[:,1:40].astype(float)
    target=dataset[:,0]
    target = numpy.reshape(target, (-1, 1))
    ds.setField('input', input)
    ds.setField('target', target)
    ds._convertToOneOfMany()
    global net
    net = buildNetwork(ds.indim, 80, ds.outdim, outclass=SoftmaxLayer)
    def train():
        back=BackpropTrainer(net,ds,learningrate = 0.0001, momentum = 0.1,verbose=True, weightdecay=0.1)
        #back.trainUntilConvergence(verbose=True)
        back.trainEpochs(100)
        with open('database.csv','r') as csvfile:
            reader=csv.reader(csvfile, delimiter=' ')
            for row in reader:
                temp= [float(row[0])]
                del(row[0])
                temp1=row
                i=0
                for value in row:
                    temp1[i]= float(value)
                    i+=1
                print(compute([temp1]))
        NetworkWriter.writeToFile(net, 'net.xml')
    train()

def compute(a):
    global net
    if len(a) == 0:
        return -1
    with open('list_person.txt','r') as lpfile:
        row_count = sum(1 for row in lpfile)
    array=list(numpy.zeros(row_count+1))
    if row_count>0:
        for i in range(0,len(a)):
            temp=list(net.activate(a[i]))
            print(temp)
            if max(temp) >= 0.8:
                array[temp.index(max(temp))] += 1
                print(temp.index(max(temp)))
        if (max(array)/len(a)) >= 0.8:
            print(len(a))
            print(max(array))
            print(max(array)/len(a))
            return array.index(max(array))
        else:
            return 0
    else:
        return 0