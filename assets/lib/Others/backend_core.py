from socket import (AF_INET, SOCK_STREAM, socket, gethostbyname, gethostname)
from zmq import (Context, REP, SNDMORE)
from numpy import (array, frombuffer)
from threading import Thread
from serial import Serial
import numpy as np
import sys

sys.path.append('assets/temp')

class Core(object):
    def __init__(self,*args):
        """ ----- """; f = open('../var/channels', 'r'); self.channels = f.read(); f.close()
        """" ---------------------------------- """; port,context = self.getPort(),Context()
        """"""; self.sockData = context.socket(REP); self.sockData.bind("tcp://*:%s" % port)
        """ --------- """; self.TARGET_RW = TARGET_RW()#; self.Filter = Filter();
        self.loop()

    def loop(self,*args):
        Thread(target = self._data_loop).start()

    def _data_loop(self,*args):
        while True:
            try:
                self.sockData.recv(); data = self._read_data()
                self.send_array(self.sockData,array(data))
            except: pass
            
    def _read_data(self,*args):
        """ ------ """; svdta,savedata = self.Tennsy.read(),[]; svdta = svdta.split('|')
        for i in range(len(svdta)): """ ------ """; savedata.append(svdta[i].split(','))
        """ ------------------------------------ """; del savedata[savedata.index([''])]
        for i in range(len(savedata)): savedata[i] = [x for x in savedata[i] if x != '']
        """ --------------------- """; data = array(savedata); data = data.astype(float)
        if len(data) == 19: return data
        else: return None
        
    def getPort(self,*args):
        f = open('port',  'rb')
        port = f.read().decode('utf-8')
        """ ------------ """; f.close()
        return port

    # Taken from https://pyzmq.readthedocs.io/en/latest/serialization.html
    # Modified by Gashpid
    def send_array(self, socket, A, flags=0, copy=True, track=False,*args):
        """send a numpy array with metadata"""
        md = dict(
            dtype = str(A.dtype),
            shape = A.shape,
        )
        socket.send_json(md, flags|SNDMORE)
        return socket.send(A, flags, copy=copy, track=track)
    
    # Taken from https://pyzmq.readthedocs.io/en/latest/serialization.html
    # Modified by Gashpid
    def recv_array(self, socket, flags=0, copy=True, track=False):
        """ ------------- recv a numpy array ------------- """
        """" --------- """; md = socket.recv_json(flags=flags)
        msg = socket.recv(flags=flags, copy=copy, track=track)
        """ ----------------------- """; buf = memoryview(msg)
        """ ------ """; A = frombuffer(buf, dtype=md['dtype'])
        return A.reshape(md['shape'])


""" ------------------------------------------------------------------------- """
""" -------------------------- TARGET READ WRITE ---------------------------- """
""" ------------------------------------------------------------------------- """


class TARGET_RW():
    def __init__(self,*args):
        """ ***** """; f = open('assets/temp/serial','rb'); self.port = f.read().decode('utf-8'); f.close()
        self.Serial = Serial(port = self.port, baudrate = 115200, timeout = None, write_timeout = None)
    
    def setBoot(self,path,*args):
        """ ------------------- """;self.Serial.close(); port = self.port
        system('cmd /c "cd %s & ampy --port %s put boot.py"'%(path,port))
        
    def getBoot(self,path,*args): pass

    def read(self,*args):
        data = self.Serial.readline().decode('utf-8')
        """ ----- """; data = data.replace('\r\n','')
        try:
            if data != '':
                data = array(data.split(',')).astype(np.float)
                return data
            else: """ ------------------ """; return None
        except: return array([0])

    def close(self,*args):
        self.Serial.close()
