from keras.datasets import imdb
(train_data, train_labels), (test_data, test_labels) = imdb.load_data(
    num_words=10000)

# print one review 'integer' sequence and the output of review (1-good,0-bad)
#print(train_data[0])
#print(train_labels[0])

# get words associated with integers
word_index = imdb.get_word_index() 
reverse_word_index = dict([(value, key) for (key, value) in word_index.items()])
decoded_review = ' '.join([reverse_word_index.get(i - 3, '?') for i in train_data[0]])
# it -3 because 0 - "padding", 1 - "start of sequence", 2 - "unknown"

# print one review sequence
#print(decoded_review)



