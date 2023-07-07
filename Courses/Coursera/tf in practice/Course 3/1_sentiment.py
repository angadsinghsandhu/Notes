import os
import numpy as np
import tensorflow as tf
import keras as k

from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences

sentences = [
    'hello how are you',
    'i an fime what about you',
    'nathing just hanging around'
]

tokenizer = Tokenizer(num_words=100, oov_token="<OOV>")
tokenizer.fit_on_texts(sentences)

word_index = tokenizer.word_index
sequence = tokenizer.texts_to_sequences(sentences)
padded = pad_sequences(sequence, maxlen=5, padding='post', truncating='post')

print(word_index)
print(sequence)
print(padded)
