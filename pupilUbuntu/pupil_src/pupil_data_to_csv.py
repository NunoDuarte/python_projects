
# coding=utf-8
import pickle
import numpy as np
import sys
import msgpack

# open the pickled file
# replace with your path to pupil_data
if sys.version_info < (3, 0):
	pupil_data = pickle.load(open("/home/nuno/recordings/2017_06_20/000/pupil_data","rb"))#,encoding='latin1') 
else:
	pupil_data = open("/home/nuno/recordings/2017_06_20/000/pupil_data","rb")


# pupil_data will be unpickled as a dictionary with three main keys
#'pupil_positions', 'gaze_positions', 'notifications'
# here we are interested in pupil_positions
#print (msgpack.unpackb(pupil_data.read()))
pupil_positions = msgpack.unpackb(pupil_data.read())
print (pupil_positions)
#pupil_positions = pupil_data['pupil_positions'] 

# uncomment the below line to see what keys are in a pupil_positions list item
# pupil_positions[0].keys() 

# to export pupil diameter in millimeters to a .csv file with timestamps frame numbers and timestamps
# as correlated columns  you can do the following:

header = ['timestamp','diameter','confidence','diameter_3D','modelConfidence']
header_str = ','.join(header)
filtered_pupil_positions = []
for i in pupil_positions:
	filtered_pupil_positions.append([i[v] for v in header])
 
np.savetxt("/home/nuno/recordings/2017_06_20/000/pupil_data.csv",filtered_pupil_positions,delimiter=",",header=header_str,comments="")
