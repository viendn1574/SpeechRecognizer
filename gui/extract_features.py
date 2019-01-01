import numpy

from scipy.io.wavfile import read
from scipy.io.wavfile import write
from python_speech_features import fbank, dct, lifter
from python_speech_features import delta
from pybrain.tools.xml import NetworkReader
import numpy as np
from scipy import signal
import GUI_Builder
from FundamentaFreq import freq_from_autocorr

net_noise=NetworkReader.readFrom('./model/net_noise.xml')
def resample(y, orig_sr, target_sr):
    print ('resample ')
    if orig_sr == target_sr:
        return y
    ratio = float(target_sr) / orig_sr
    n_samples = int(np.ceil(y.shape[-1] * ratio))
    y_hat = signal.resample(y, n_samples, axis=-1)
    ret = np.ascontiguousarray(y_hat, dtype=y.dtype)
    print ('resample end')
    return ret

def reduce_noise(filename):
    print ('reduce noise')
    namefile = filename.replace(".wav", "")
    lowpass = 21 # Remove lower frequencies.
    highpass = 9000 # Remove higher frequencies.
    (Frequency, array) = read(filename)
    array_16=resample(array,44100,16000)
    lf = numpy.fft.rfft(array_16)
    lf[:lowpass]= 0 # low pass filter
    lf[44:77]= 0# line noise
    lf[highpass:]= 0 # high pass filter
    nl = numpy.fft.irfft(lf)
    ns = numpy.column_stack(nl).ravel().astype(numpy.int16)
    write(namefile+'_filtered.wav', 16000,ns)
    print ('reduce noise end')

def extract_mfcc(signal,samplerate=16000,winlen=0.025,winstep=0.01,numcep=13,
         nfilt=26,nfft=512,lowfreq=0,highfreq=None,preemph=0.97,ceplifter=22,appendEnergy=True,
         winfunc=lambda x:numpy.ones((x,))):
    print ('extract mfcc')
    feat,energy = fbank(signal,samplerate,winlen,winstep,nfilt,nfft,lowfreq,highfreq,preemph,winfunc)
    feat = numpy.log(feat)
    feat = dct(feat, type=2, axis=1, norm='ortho')[:,:numcep]
    feat = lifter(feat,ceplifter)
    if appendEnergy:
        feat=numpy.c_[feat, numpy.log(energy)] # append cepstral coefficient with log of frame energy
    print ('extract mfcc end')
    return feat, numpy.log(energy)

def isNoise(a):
    global net
    result=net_noise.activate(a)
    if result[0]>=0.7:
        return 1
    else:
        return 0

def extract_features(filename):
    print ('extract features')
    reduce_noise(filename)
    namefile = filename.replace(".wav", "")
    rate,sig = read(namefile+'_filtered.wav')  # Y gives

    mfcc_feat, energy = extract_mfcc(sig,appendEnergy=False,numcep=12)
    #GUI_Builder.object.canvas_show(sig,mfcc_feat)
    delta_mfcc = delta(mfcc_feat, 2)
    delta_mfcc_2 = delta(delta_mfcc, 2)

    dataraw=numpy.c_[mfcc_feat,delta_mfcc]
    dataraw=numpy.c_[dataraw,delta_mfcc_2]
    count=0
    for j in range(0,len(mfcc_feat)):
        if (isNoise(dataraw[count])==1):
            dataraw=numpy.delete(dataraw,count,0)
            energy=numpy.delete(energy,count,0)
        else:
            count+=1
    dataraw=numpy.c_[dataraw,energy]
    f0=freq_from_autocorr(sig,rate)
    data=[]
    for j in range(0,len(dataraw)-3,2):
        datatemp=dataraw[j:j+3,:]
        data.append(numpy.append(datatemp.ravel(0),f0))
    print ('extract features end')
    return data
