from scipy.fft import fft,fftfreq,fftshift
from scipy import signal
import numpy as np

class Filter():
    def __init__(self,fs,*args):
        self.fs = fs

    def build(self,filters,*args):
        """ ****** """; self.fil = []
        for i in range(len(filters)):
            if len(filters[i]) == 5: self.fil.append(self.BandPass(filters[i]))
            if len(filters[i]) == 4: self.fil.append(self.Notch(filters[i]))
        self.fil.append(self.HighPass(6,0.01))

    def apply(self,fil,data,*args):
        sigfil,data = [],signal.filtfilt(self.fil[len(self.fil)-1][0], self.fil[len(self.fil)-1][1], data)
        for i in range(len(self.fil)-1):
            if self.fil[i][0] == fil[i]:
                sigfil.append(signal.filtfilt(self.fil[i][1], self.fil[i][2], data))
        return sigfil
    
    def HighPass(self,order,fc,*args):  
        b, a = signal.butter(order, (2*fc)/self.fs, 'high', analog=False)
        return [b,a]

    def BandPass(self,fil,*args):
        if len(fil) == 5:
            b, a = signal.butter(fil[1], np.array([(2*fil[2])/self.fs, (2*fil[3])/self.fs]), 'bandpass', analog=False)
            return [fil[4],b,a]

    def Notch(self,fil,*args):
        b, a = signal.iirnotch(fil[1], fil[2], self.fs)
        return [fil[3],b,a]

class sigTools():
    def __init__(self,filt,*args):
        self.filfit = Filter(240)
        self.filfit.build(filt)

    def FFT(self,data,fs,log=False,normalize=False,*args):
        """ ********************* """; N = len(data); T = 1/fs
        """ ***** """; x = np.linspace(0,N*T,N,endpoint=False)
        """ ************************************ """; y = data
        """ **************************** """; yf = abs(fft(y))
        """ *************************** """; xf = fftfreq(N,T)
        """ *************************** """; xf = fftshift(xf)
        """ *************************** """; yf = fftshift(yf)
        """""";xf,yf = np.array(xf[N//2:]),np.array(yf[N//2:])
        if log == True: yf = 20*np.log10(yf, dtype ='float64')
        if normalize == True:yf=yf/yf[list(yf).index(max(yf))]
        return xf,yf

    def PWELCH(self,data,fs,*args):
        f, Pxx_den = signal.welch(data, fs, nperseg=fs)
        return f, Pxx_den
    
