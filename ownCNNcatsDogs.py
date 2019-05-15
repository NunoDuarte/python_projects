import matplotlib.pyplot as plt
import numpy as np
#from firstKagglecode import process_test_data #this will make it run process_test_data every time you run the program
import catsDogsCNN.model as model # this will make you train the model every time you run the program

# if you dont have this file yet
#test_data = process_test_data()
# if you already have it
test_data = np.load('test_data.npy')

IMG_SIZE = 50

fig = plt.figure()

# show the last 12 pictures
for num, data in enumerate(test_data[:12]):
    # cat: [1, 0]
    # dog: [0, 1]
    
    img_num = data[1]
    img_data = data[0]
    
    y = fig.add_subplot(3, 4, num+1)
    orig = img_data
    data = img_data.reshape(IMG_SIZE, IMG_SIZE, 1)

    model_out = model.predict([data])[0]
    
    if np.argmax(model_out) == 1: str_label='Dog'
    else: str_label='Cat'
    
    y.imshow(orig, cmap='gray')
    plt.title(str_label)
    y.axes.get_xaxis().set_visible(False)
    y.axes.get_yaxis().set_visible(False)
    
plt.show()
    
    
    