import numpy as np
import tensorflow as tf
from tensorflow import keras as k
import datetime

then = datetime.datetime.now()

# creating callback class


class myCallback(k.callbacks.Callback):
    def on_epoch_end(self, epoch, logs={}):
        if (logs.get('accuracy') > 0.9):
            print("\nLoss is low and acuuuracy above 90%...cancelling training...")
            self.model.stop_training = True


# instantiating class
callbacks = myCallback()

# loading MNIST FASHION dataset from tensorflow
fashion_mnist = k.datasets.fashion_mnist
(train_images, train_labels), (test_images,
                               test_labels) = fashion_mnist.load_data()

# normalizing data
train_images = train_images / 255.0
test_images = test_images / 255.0

# creating NN Model
model = k.Sequential([k.layers.Flatten(),
                      k.layers.Dense(256, activation=tf.nn.relu),
                      k.layers.Dense(1024, activation=tf.nn.relu),
                      k.layers.Dense(512, activation=tf.nn.relu),
                      k.layers.Dense(128, activation=tf.nn.relu),
                      k.layers.Dense(10, activation=tf.nn.softmax)])

#compiling and training
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy', metrics=['accuracy'])
model.fit(train_images, train_labels, epochs=25, callbacks=[callbacks])

# evaluating model using evaluate
print('\nTest Data : \n')
model.evaluate(test_images, test_labels)

print("\ntime taken to execute {}sec".format(
    (datetime.datetime.now() - then)//datetime.timedelta(seconds=1))
)
