import matplotlib.pyplot as plt
import os
import io
import numpy as np
import tensorflow as tf
import keras as k

from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
import tensorflow_datasets as tfds

# getting imdb reviews data
# download_dir = 'D:\Code\AI\datasets'
# tfds.download.DownloadManager(
#     download_dir='D:\Code\AI\datasets', extract_dir='D:\Code\AI\datasets'
# )
imdb, info = tfds.load("imdb_reviews", with_info=True,
                       as_supervised=True, data_dir='D:\Code\AI\datasets', download=False)

# splitting data and instantiating lists
train_data, test_data = imdb['train'], imdb['test']
training_sentences, training_labels = [], []
testing_sentences, testing_labels = [], []

for s, l in train_data:
    training_sentences.append(str(s.numpy().decode('utf8')))
    training_labels.append(l.numpy())

for s, l in test_data:
    testing_sentences.append(str(s.numpy().decode('utf8')))
    testing_labels.append(l.numpy())

print("\ntrain data sentences : ")
print(training_sentences[:10])
print("\ntrain data labels : ")
print(training_labels[:10])
print("\ntest set length : {}".format(len(training_labels)))

training_labels_final = np.array(training_labels)
testing_labels_final = np.array(testing_labels)

# defining hyperparameters
vocab_size = 10000
embedding_dim = 64
max_length = 120
trunc_type = 'post'
oov_tok = "<OOV>"

# creating tokens for training
tokenizer = Tokenizer(num_words=vocab_size, oov_token=oov_tok)
tokenizer.fit_on_texts(training_sentences)

word_index = tokenizer.word_index
sequence = tokenizer.texts_to_sequences(training_sentences)
padded = pad_sequences(sequence, maxlen=max_length, truncating=trunc_type)

# creating testing tokens for similar data
testing_sequences = tokenizer.texts_to_sequences(testing_sentences)
testing_padded = pad_sequences(
    testing_sequences, maxlen=max_length, truncating=trunc_type)

# printing out the paddings
print("\n\nword index : ")
print(word_index)
print("\n\nsequence : ")
print(sequence)
print("\n\ntraining set padded : " + str(padded) +
      "\n\ntesting set padded : " + str(testing_padded))


class MyCallback(tf.keras.callbacks.Callback):  # creating callback class
    def on_epoch_end(self, epoch, logs={}):
        if (logs.get('accuracy') > 0.99):
            print("accuracy exceeded 99%...Stopping Training...")
            self.model.stop_training = True


# instantiating callback
callbacks = MyCallback()

# creating NN Model
# different models are implemented here

# for single layer LSTM only keep #2 uncommented
# for single layer GRU only keep #3 uncommented
# for multi layer LSTM keep #2 and #1 uncommented
# for Convolution in sequence keep #4 and #5 uncommented


model = k.Sequential([
    k.layers.Embedding(vocab_size, embedding_dim, input_length=max_length),
    # k.layers.Bidirectional(k.layers.LSTM(64, return_sequences=True)),  # 1
    # k.layers.Bidirectional(k.layers.LSTM(32)),  # 2
    # k.layers.Bidirectional(k.layers.GRU(32)),  # 3
    k.layers.Conv1D(128, 5, activation='relu'),  # 4
    k.layers.GlobalAveragePooling1D(),  # 5
    k.layers.Dense(64, activation='relu'),
    k.layers.Dense(1, activation='sigmoid'),
])

# summary
print("Model Summary : \n")
model.summary()

model.compile(
    loss='binary_crossentropy',
    optimizer=k.optimizers.Adam(learning_rate=0.01),
    metrics=['accuracy']
)

history = model.fit(
    padded,
    training_labels_final,
    epochs=10,
    validation_data=(testing_padded, testing_labels_final)
)


def plot_graphs(history, string):
    plt.plot(history.history[string])
    plt.plot(history.history['val_'+string])
    plt.xlabel("Epochs")
    plt.ylabel(string)
    plt.legend([string, 'val_'+string])
    plt.show()


plot_graphs(history, 'accuracy')
plot_graphs(history, 'loss')
