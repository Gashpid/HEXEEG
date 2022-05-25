import zmq
import numpy
port = "5555"

context = zmq.Context()
print ("Connecting to server...")
socket = context.socket(zmq.REQ)
socket.connect ("tcp://localhost:%s" % port)

def recv_array(socket, flags=0, copy=True, track=False):
    """recv a numpy array"""
    md = socket.recv_json(flags=flags)
    msg = socket.recv(flags=flags, copy=copy, track=track)
    buf = memoryview(msg)
    A = numpy.frombuffer(buf, dtype=md['dtype'])
    return A.reshape(md['shape'])

for request in range (1,1000):
    print('0')
    print ("Sending request ", request,"...")
    socket.send_string("Hello")
    #  Get the reply.
    message = recv_array(socket)
    print ("Received reply ", request, "[", message, "]")

