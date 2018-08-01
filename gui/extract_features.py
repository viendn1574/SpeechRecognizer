import numpy
from scipy.io import wavfile
from python_speech_features import fbank, dct, lifter
from python_speech_features import delta
from pybrain.tools.xml import NetworkReader
from sklearn import decomposition
from sklearn.preprocessing import StandardScaler

net_noise=NetworkReader.readFrom('net_noise.xml')

def extract_mfcc(signal,samplerate=16000,winlen=0.025,winstep=0.01,numcep=13,
         nfilt=26,nfft=512,lowfreq=0,highfreq=None,preemph=0.97,ceplifter=22,appendEnergy=True,
         winfunc=lambda x:numpy.ones((x,))):

    feat,energy = fbank(signal,samplerate,winlen,winstep,nfilt,nfft,lowfreq,highfreq,preemph,winfunc)
    feat = numpy.log(feat)
    feat = dct(feat, type=2, axis=1, norm='ortho')[:,:numcep]
    feat = lifter(feat,ceplifter)
    if appendEnergy:
        feat=numpy.c_[feat, numpy.log(energy)] # append cepstral coefficient with log of frame energy
    return feat

def isNoise(a):
    global net
    result=net_noise.activate(a)
    if result[0]>=0.7:
        return 1
    else:
        return 0

def extract_features(filename):
    pca = decomposition.PCA(n_components=18)
    rate,sig = wavfile.read(filename)  # Y gives
    mfcc_feat = extract_mfcc(sig,appendEnergy=True,numcep=12)
    delta_mfcc = delta(mfcc_feat, 2)
    delta_mfcc_2 = delta(delta_mfcc, 2)

    dataraw=numpy.c_[mfcc_feat,delta_mfcc]
    dataraw=numpy.c_[dataraw,delta_mfcc_2]
    count=0
    for j in range(0,len(mfcc_feat)):
        if (isNoise(dataraw[count])==1):
            dataraw=numpy.delete(dataraw,count,0)
        else:
            count+=1
    return dataraw

    # datatemp=[]
    # if len(dataraw)>=80:
    #     for j in range(0,len(dataraw)-79,50):
    #         data=dataraw[j:j+80,:]
    #         x_std = StandardScaler().fit_transform(data)
    #         datatemp.append((pca.fit_transform(x_std)).ravel(0))
    # return datatemp
