from scipy.signal import (butter, iirnotch, filtfilt)
from warnings import filterwarnings
from serial import Serial
from numpy import array
from os import system


filterwarnings("ignore")


class Tennsy():
    def __init__(self,*args):
        f = open('../temp/serial','rb'); self.port = f.read().decode('utf-8'); f.close()
        self.Serial = Serial(port = self.port, baudrate = 115200, timeout = None, write_timeout = None)

    def setBoot(self,path,*args):
        """ ------------------- """;self.Serial.close(); port = self.port
        system('cmd /c "cd %s & ampy --port %s put boot.py"'%(path,port))
        
    def getBoot(self,path,*args): pass

    def read(self,*args):
        data = self.Serial.readline().decode('utf-8')
        """ ----- """; data = data.replace('\r\n','')
        if data != '': """ --------- """; return data
        else: """ ------------------ """; return None

    def close(self,*args): self.Serial.close()

class Filter():
    def __init__(self,*args):
        f = open('../var/fs','r'); self.fs = float(f.read()); f.close()
        self.filters,self.filtername = [],[]
        f = open('../var/filters','r')
        while(True):
            line = f.readline()
            line = line.replace('\n','')
            self.filters.append(line.split(','))
            if not line:
                break
        f.close()
        del line

        for i in range(len(self.filters)):
            if self.filters[i][len(self.filters[i])-1] != '': """ ------------------------------- """; self.filtername.append(self.filters[i][len(self.filters[i])-1])
            if self.filters[i][0] == 'BandPass': self.filters[i] = self.BandPass_designer(int(self.filters[i][1]),float(self.filters[i][2]),float(self.filters[i][3]))
            if self.filters[i][0] == 'Notch': """ -------------------- """; self.filters[i] = self.Notch_designer(float(self.filters[i][1]),float(self.filters[i][2]))
        self.filters.remove([''])
        
    def BandPass_designer(self,order,LpFc,HpFc,*args,help='order=filter order,LpFc=cutoff low frequency,HpFc=cutoff high frequency'):
        b, a = butter(order, array([(2*LpFc)/self.fs, (2*HpFc)/self.fs]), 'bandpass', analog=False)
        return [b,a]

    def Notch_designer(self,f0,Q,*args,help='f0=Frequency to be removed from signal (Hz), Q=Quality factor'):
        b, a = iirnotch(f0, Q, self.fs)
        return [b,a]

    def Apply(self,data,flt,*args):
        try:
            index = self.filtername.index(flt)
            if flt == self.filtername[index]:
                b,a = self.filters[index]
                return filtfilt(b,a,data)
        except: return None

