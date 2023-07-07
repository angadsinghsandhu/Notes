
import matplotlib.pyplot as plt
import tensorflow as tf
import tensorflow_datasets as tfds
import tensorflow.keras as k
import numpy as np

# EXTRACT
dataset = tfds.load('mnist', split='train', with_info=True)

# TRANSFORM
dataset.shuffle(100)

# LOAD
for data in dataset.take(1):
    image, label = data['image'], data['label']
    plt.imshow(image.numpy()[:, :, 0].astype(np.float32),
               cmap=plt.get_cmap("grey"))
    print("Label : {}".format(label.numpy()))
    plt.show()
