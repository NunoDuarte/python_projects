#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import tensorflow as tf
import numpy as np

IMG_PX = 50
HM_SLICES = 20

n_classes = 2 # cancer or no cancer
batch_size = 10

x = tf.placeholder('float')
y = tf.placeholder('float')

keep_rate = 0.8
keep_prob = tf.placeholder(tf.float32)

def conv3d(x, W):
    return tf.nn.conv3d(x, W, strides=[1,1,1,1,1], padding='SAME')

def maxpool3d(x):
    #                        size of window     movement of window
    return tf.nn.max_pool3d(x, ksize=[1,2,2,2,1], strides=[1,2,2,2,1], padding='SAME')

def convolutional_neural_network(x):
    weights = {
        'w_conv1':tf.Variable(tf.random_normal([3,3,3,1,32])), 
        'w_conv2':tf.Variable(tf.random_normal([3,3,3,32,64])),
        'w_fc':tf.Variable(tf.random_normal([54080,1024])),            
        'out':tf.Variable(tf.random_normal([1024, n_classes]))}     

    biases = {
        'b_conv1':tf.Variable(tf.random_normal([32])),
        'b_conv2':tf.Variable(tf.random_normal([64])),
        'b_fc':tf.Variable(tf.random_normal([1024])),
        'out':tf.Variable(tf.random_normal([n_classes]))}
    
    x = tf.reshape(x, shape=[-1, IMG_PX, IMG_PX, HM_SLICES, 1])
    
    conv1 = tf.nn.relu(conv3d(x, weights['w_conv1']) + biases['b_conv1'])
    conv1 = maxpool3d(conv1)

    conv2 = tf.nn.relu(conv3d(conv1, weights['w_conv2']) + biases['b_conv2'])
    conv2 = maxpool3d(conv2)

    fc = tf.reshape(conv2, [-1, 54080])
    fc = tf.nn.relu(tf.matmul(fc, weights['w_fc']) + biases['b_fc'])
    
    # dropout layer
    fc = tf.nn.dropout(fc, keep_rate)
    
    output = tf.matmul(fc, weights['out']) + biases['out']
    
    return output

def train_neural_network(x):
    
    much_data = np.load('muchdata-50-50-20.npy')
    train_data = much_data[:-100]
    validation_data = much_data[-100:]
    
    prediction = convolutional_neural_network(x)
    cost = tf.reduce_mean( tf.nn.softmax_cross_entropy_with_logits(logits=prediction, labels=y) )
    optimizer = tf.train.AdamOptimizer().minimize(cost)
    
    hm_epochs = 10
    with tf.Session() as sess:
        # OLD:
        #sess.run(tf.initialize_all_variables())
        # NEW:
        sess.run(tf.global_variables_initializer())

        for epoch in range(hm_epochs):
            epoch_loss = 0
            success_total = 0
            attempt_total = 0
            for data in train_data:
                attempt_total += 1
                try:
                    X = data[0]
                    Y = data[1]
                    _, c = sess.run([optimizer, cost], feed_dict={x: X, y: Y})
                    epoch_loss += c
                    success_total += 1
                except Exception as e:
                    pass
                    
            print('Epoch', epoch+1, 'completed out of',hm_epochs,'loss:',epoch_loss,
                 'success rate:', success_total/attempt_total)

        # check if the index of the prediction is the same for the real value (y)
        # correct? [1,0,0] = [1,0,0] - YES!
        correct = tf.equal(tf.argmax(prediction, 1), tf.argmax(y, 1))

        accuracy = tf.reduce_mean(tf.cast(correct, 'float'))
        print('Accuracy:',accuracy.eval({x:[i[0] for i in validation_data], y:[i[1] for i in validation_data]}))

train_neural_network(x)

