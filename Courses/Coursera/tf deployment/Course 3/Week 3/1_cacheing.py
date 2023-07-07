import tensorflow as tf
import tensorflow.keras as k
import tensorflow_datasets as tfds

# loading dataset
dataset = tfds.load('cats_vs_dogs', split=tfds.Split.TRAIN)

# In-Memory Cache
train_dataset = dataset.cache()
'''model.fit(train_dataset, epochs=...)'''

# Disk Memory Cache
train_dataset = dataset.cache(filename='cache')
'''model.fit(train_dataset, epochs=...)'''
