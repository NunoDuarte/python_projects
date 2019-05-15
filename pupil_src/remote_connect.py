import zmq
from time import sleep,time
context =  zmq.Context()
socket = context.socket(zmq.REQ)
# set your ip here
socket.connect('tcp://10.0.21.96:42877')
t= time()
socket.send_string('t')
print (socket.recv())
print ('Round trip command delay:', time()-t)
print ('If you need continous syncing and/or less latency look at pupil_sync.')
sleep(1)
socket.send_string('R')
print (socket.recv())
sleep(5)
socket.send_string('r')
print (socket.recv())
