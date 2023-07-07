import matplotlib.pyplot as plt
import os
import io
import numpy as np
import tensorflow as tf
import keras as k

from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
import tensorflow_datasets as tfds


class MyCallback(tf.keras.callbacks.Callback):  # creating callback class
    def on_epoch_end(self, epoch, logs={}):
        if (logs.get('accuracy') > 0.99):
            print("accuracy exceeded 99%...Stopping Training...")
            self.model.stop_training = True


# instantiating callback
callbacks = MyCallback()

# defining hyperparameters
vocab_size = 10000
embedding_dim = 64
max_length = 120
trunc_type = 'post'
oov_tok = "<OOV>"

# data = '''In the town of Athy one Jeremy Lanigan \n Battered away til he hadnt a pound. \nHis father died and made him a man again \n Left him a farm and ten acres of ground. \nHe gave a grand party for friends and relations \nWho didnt forget him when come to the wall, \nAnd if youll but listen Ill make your eyes glisten \nOf the rows and the ructions of Lanigans Ball. \nMyself to be sure got free invitation, \nFor all the nice girls and boys I might ask, \nAnd just in a minute both friends and relations \nWere dancing round merry as bees round a cask. \nJudy ODaly, that nice little milliner, \nShe tipped me a wink for to give her a call, \nAnd I soon arrived with Peggy McGilligan \nJust in time for Lanigans Ball. \nThere were lashings of punch and wine for the ladies, \nPotatoes and cakes; there was bacon and tea, \nThere were the Nolans, Dolans, OGradys \nCourting the girls and dancing away. \nSongs they went round as plenty as water, \nThe harp that once sounded in Taras old hall,\nSweet Nelly Gray and The Rat Catchers Daughter,\nAll singing together at Lanigans Ball. \nThey were doing all kinds of nonsensical polkas \nAll round the room in a whirligig. \nJulia and I, we banished their nonsense \nAnd tipped them the twist of a reel and a jig. \nAch mavrone, how the girls got all mad at me \nDanced til youd think the ceiling would fall. \nFor I spent three weeks at Brooks Academy \nLearning new steps for Lanigans Ball. \nThree long weeks I spent up in Dublin, \nThree long weeks to learn nothing at all,\n Three long weeks I spent up in Dublin, \nLearning new steps for Lanigans Ball. \nShe stepped out and I stepped in again, \nI stepped out and she stepped in again, \nShe stepped out and I stepped in again, \nLearning new steps for Lanigans Ball. \nBoys were all merry and the girls they were hearty \nAnd danced all around in couples and groups, \nTil an accident happened, young Terrance McCarthy \nPut his right leg through miss Finnertys hoops. \nPoor creature fainted and cried Meelia murther, \nCalled for her brothers and gathered them all. \nCarmody swore that hed go no further \nTil he had satisfaction at Lanigans Ball. \nIn the midst of the row miss Kerrigan fainted, \nHer cheeks at the same time as red as a rose. \nSome of the lads declared she was painted, \nShe took a small drop too much, I suppose. \nHer sweetheart, Ned Morgan, so powerful and able, \nWhen he saw his fair colleen stretched out by the wall, \nTore the left leg from under the table \nAnd smashed all the Chaneys at Lanigans Ball. \nBoys, oh boys, twas then there were runctions. \nMyself got a lick from big Phelim McHugh. \nI soon replied to his introduction \nAnd kicked up a terrible hullabaloo. \nOld Casey, the piper, was near being strangled. \nThey squeezed up his pipes, bellows, chanters and all. \nThe girls, in their ribbons, they got all entangled \nAnd that put an end to Lanigans Ball.'''
f = open(f"D:\Code\AI\datasets\irish_poem\irish_poem.txt", "r")
data = f.read()

corpus = data.lower().split("\n")

# creating tokenizer
tokenizer = Tokenizer(num_words=vocab_size, oov_token=oov_tok)
tokenizer.fit_on_texts(corpus)
total_words = len(tokenizer.word_index) + 1
word_index = tokenizer.word_index

# creating sequence for training
input_sequences = []
for line in corpus:
    token_list = tokenizer.texts_to_sequences([line])[0]
    for i in range(1, len(token_list)):
        sequence = token_list[:i]
        input_sequences.append(sequence)

# padding sequences
max_sequence_len = max([len(x) for x in input_sequences])
input_sequences = np.array(pad_sequences(
    input_sequences, maxlen=max_sequence_len, padding='pre'))

# creating predictions and labels
xs, labels = input_sequences[:, :-1], input_sequences[:, -1]
ys = k.utils.to_categorical(labels, num_classes=total_words)

print('\n')
print(tokenizer.word_index)
print('\n')
print(xs[6])
print('\n')

model = k.Sequential([
    k.layers.Embedding(total_words, 100, input_length=max_sequence_len - 1),
    k.layers.Bidirectional(k.layers.LSTM(150)),
    k.layers.Dense(total_words, activation='softmax')
])

model.compile(
    loss='categorical_crossentropy',
    optimizer=k.optimizers.Adam(learning_rate=0.01),
    metrics=['accuracy']
)

history = model.fit(xs, ys, epochs=100, verbose=1)


def plot_graph(history, str):
    plt.plot(history.history[str])
    plt.xlabel("Number of Epochs")
    plt.ylabel(str)
    plt.show()


plot_graph(history, 'accuracy')

text = "I love you"
next_words = 10

for i in range(next_words):
    token_list = tokenizer.texts_to_sequences([text])[0]
    token_list = pad_sequences(
        [token_list], maxlen=max_sequence_len-1, padding='pre')

    predicted = model.predict_classes(token_list, verbose=1)
    output = ""

    for word, index in tokenizer.word_index.items():
        if index == predicted:
            out = word
            break

    text += " " + out

print(text)
