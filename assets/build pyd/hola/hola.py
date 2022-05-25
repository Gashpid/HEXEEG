import matplotlib.pyplot as plt
import serial
import time
plt.ion()

port = 'COM3'
SerialPort = serial.Serial(port, 2000000)

data = []

init = time.time()


plt.plot(data)
for i in range(1000):
    readed = SerialPort.readline()
    readed = readed.decode('utf-8')
    readed = readed.replace('\r\n','')
    data.append(readed.split(','))
    try: plt.plot(float(data[i][0]))
    except: pass
    plt.pause(0.0001)
    plt.show()


##end = time.time()
##
##print(end-init)
##dat = data[2:]
##
##vec = [dat[i][0] for i in range(len(dat))]
##vec = [float(vec[i]) for i in range(len(vec))]
##
##plt.plot(vec)









