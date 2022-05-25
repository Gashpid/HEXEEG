from scipy.fft import fft,fftfreq,fftshift
from scipy import signal
import numpy as np
import nolds as nd


##########################################################################################################################
################################################ LOAD DATA & MODULES #####################################################
##########################################################################################################################
class Load():
    def __init__(self,*args): pass

    def filters(self,del_band=None,*args):
        f,ix = open('assets/var/filters','r'),[]
        filters = f.read(); f.close()
        filters = filters.split('\n')
        aux = []
        
        for i in range(len(filters)):
            filters[i],aux = filters[i].split(','),[]
    
            for k in range(len(filters[i])):
                try: aux.append(float(filters[i][k]))
                except: aux.append(filters[i][k])
                
            for k in range(len(del_band)):
                if filters[i][len(filters[i])-1] != del_band[k]: filters[i] = aux
                else: ix.append(i)

        for i in range(len(ix)): filters.pop(ix[i]-i)
        
        return filters

##########################################################################################################################
#################################################### FILTERING MODULE ####################################################
##########################################################################################################################
class Filter():
    def __init__(self,fs,*args):
        self.fs = fs

    def build(self,filters,*args):
        self.fil = []
        for i in range(len(filters)-1):
            if len(filters[i]) == 5:
                b,a = self.BandPass(filters[i])
                """ """; self.fil.append([b,a])
            if len(filters[i]) == 4:
                b, a = self.Notch(filters[i])
                """""";self.fil.append([b,a])

    def apply(self,data,Notch=False,*args):
        sigfil = []
        
        if Notch == True: data = signal.filtfilt(self.fil[len(self.fil)-1][0], self.fil[len(self.fil)-1][1], data)

        for i in range(len(self.fil)):
                sigfil.append(signal.filtfilt(self.fil[i][0], self.fil[i][1], data))

        return sigfil
    
    def HighPass(self,order,fc,*args):  
        b, a = signal.butter(order, (2*fc)/self.fs, 'high', analog=False)
        return [b,a]

    def BandPass(self,fil,*args):
        b, a = signal.butter(fil[1], np.array([(2*fil[2])/self.fs, (2*fil[3])/self.fs]), 'bandpass', analog=False)
        return b,a

    def Notch(self,fil,*args):
        b, a = signal.iirnotch(f0=fil[1], Q=fil[2], fs=self.fs)
        return b,a

##########################################################################################################################
##################################################### MAIN MODULE ########################################################
##########################################################################################################################
class sigTools():
    def __init__(self,fs,del_band=None,*args):
        self.fs = fs; LoadDM = Load()
        filt = LoadDM.filters(del_band=del_band)
        self.filfit = Filter(fs)
        self.filfit.build(filt)

    def delZeros(self,data,*args):
        index = []
        for i in range(len(data)):
            if data[i] == 0: index.append(i)
        return np.delete(data,index)

    def FFT(self,data,log=False,normalize=False,*args):
        """ ********************* """; N = len(data); T = 1/self.fs
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

    def Pwelch(self,data,*args):
        f, Pxx_den = signal.welch(data, self.fs, nperseg=self.fs)
        return f, Pxx_den

    def coh(self,u,y,*args):
        f,Pxx_den = signal.welch(y,fs=self.fs, window='hann', nperseg=len(u), average='mean')
        _,Pff_den = signal.welch(u,fs=self.fs, window='hann', nperseg=len(u), average='mean')
        _,Pfx_den = signal.csd(u,y,fs=self.fs, window='hann', nperseg=len(u), average='mean')
        cohn = abs(Pfx_den)**2; cohdn = np.dot(Pxx_den,Pff_den); coh = cohn/cohdn
        coh = np.transpose(coh)
        return coh

    def lyap(self,data,*args):
        return nd.lyap_e(data,matrix_dim=2)

    def corrDim(self,data,*args):
        return nd.corr_dim(data,emb_dim=len(data)-1)

    def wavEntropy(self,data,*args):
        return nd.sampen(data)

    def TaBaRatio(self,Theta,Beta,mean=False,*args):
        if mean: return np.mean(Theta/Beta)
        else: return Theta/Beta
        
        
    
