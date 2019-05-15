"""
Receive data from Pupil server broadcast over TCP
test script to see what the stream looks like
and for debugging
"""
import zmq
import json
 
#network setup
port = "50020"
context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://127.0.0.1:"+port)
 
# recv all messages
socket.setsockopt(zmq.SUBSCRIBE, b'')
# recv just pupil postions
# socket.setsockopt(zmq.SUBSCRIBE, 'pupil_positions')
# recv just gaze postions
# socket.setsockopt(zmq.SUBSCRIBE, 'gaze_positions')
print('ok')
while True:
    topic,msg =  socket.recv_string()
    print('ok')
    msg = json.loads(msg)
    print ("\n\n",topic,":\n",msg)
     
    
    
# import zmq
# import json
# 
# #network setup
# port = "50020"
# context = zmq.Context()
# socket = context.socket(zmq.SUB)
# socket.connect("tcp://127.0.0.1:"+port)
# #get gaze data only
# socket.setsockopt(zmq.SUBSCRIBE, b'gaze_positions')
# 
# # specify the name of the surface you want to use
# while True:
#     topic,msg =  socket.recv_multipart()
#     gaze_positions = json.loads(msg)
#     for gaze_position in gaze_positions:
#         print(gaze_position)
#     
#     