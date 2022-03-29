"""Example program to demonstrate how to read string-valued markers from LSL."""

from pylsl import StreamInlet, resolve_stream

# first resolve a marker stream on the lab network
print("looking for a marker stream...")
# type = 'Pupil Capture'
# name = 'Gaze Primitive Data' or 'Gaze Python Representation'
streams = resolve_stream('name', 'Gaze Python Representation')
print("connected")

# create a new inlet to read from the stream
inlet = StreamInlet(streams[0])

while True:
    # get a new sample (you can also omit the timestamp part if you're not
    # interested in it)
    sample, timestamp = inlet.pull_sample()
    print("got %s at time %s" % (sample[0], timestamp))
    #print("norm pos x %s and norm pos y %s" % (sample[3], sample[4]))