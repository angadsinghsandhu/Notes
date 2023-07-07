import os
import datetime
import numpy as np
import tensorflow as tf
from tensorflow_core.python.keras.applications.inception_v3 import InceptionV3
from tensorflow import keras as k
from tensorflow_core.python.keras import layers
from tensorflow_core.python.keras import Model
from matplotlib import pyplot as plt
from keras.preprocessing.image import ImageDataGenerator
from tensorflow_core.python.keras.api.keras.preprocessing import image

# downloaded and unzipped InceptionNetV3 weights from
# "https://storage.googleapis.com/mledu-datasets/inception_v3_weights_tf_dim_ordering_tf_kernels_notop.h5"
# already in directory

# Also using the cats-vs-dogs dataset

# storing starting time
then = datetime.datetime.now()

local_weights_file = 'D:/Code/AI/models/InceptionV3/inception_v3_weights_tf_dim_ordering_tf_kernels_notop.h5'

pre_trained_model = InceptionV3(input_shape=(150, 150, 3),
                                include_top=False,
                                weights=None)

pre_trained_model.load_weights(local_weights_file)

for layer in pre_trained_model.layers:
    layer.trainable = False

last_layer = pre_trained_model.get_layer('mixed7')
print('\nlast layer output shape: ', last_layer.output_shape)
last_output = last_layer.output

# Adding dinal trainable layers

# Flatten the output layer to 1 dimension
x = layers.Flatten()(last_output)
# Add a fully connected layer with 1,024 hidden units and ReLU activation
x = layers.Dense(1024, activation='relu')(x)
# Add a dropout rate of 0.2
x = layers.Dropout(0.2)(x)
# Add a final sigmoid layer for classification
x = layers.Dense(1, activation='sigmoid')(x)

model = k.Model(pre_trained_model.input, x)

model.compile(optimizer=k.optimizers.RMSprop(lr=0.0001),
              loss='binary_crossentropy',
              metrics=['accuracy'])

# creating callback class


class MyCallback(k.callbacks.Callback):
    def on_epoch_end(self, epoch, logs={}):
        if (logs.get('accuracy') > 0.99):
            print("accuracy exceeded 99%...Stopping Training...")
            self.model.stop_training = True


# instantiating callback
callbacks = MyCallback()

# defining directories
base_dir = f'D:\Code\AI\datasets\cats_and_dogs_filtered'
train_dir = os.path.join(base_dir, 'train')
test_dir = os.path.join(base_dir, 'validation')

# defining train directories
train_cats_dir = os.path.join(train_dir, 'cats')
train_dogs_dir = os.path.join(train_dir, 'dogs')

# defining test directories
test_cats_dir = os.path.join(test_dir, 'cats')
test_dogs_dir = os.path.join(test_dir, 'dogs')

# file names
fh_train_cats = os.listdir(train_cats_dir)
fh_train_dogs = os.listdir(train_dogs_dir)

# list names
print("\n\n")
print(fh_train_cats[:10])
print(fh_train_dogs[:10])

# number of images
print("\n")
print("cats train set : " + str(len(train_cats_dir)) + " images\n")
print("dogs train set : " + str(len(train_dogs_dir)) + " images\n")
print("cats test set : " + str(len(test_cats_dir)) + " images\n")
print("dogs test set : " + str(len(test_dogs_dir)) + " images\n")

# Add our data-augmentation parameters to ImageDataGenerator
train_datagen = ImageDataGenerator(rescale=1./255.,
                                   rotation_range=40,
                                   width_shift_range=0.2,
                                   height_shift_range=0.2,
                                   shear_range=0.2,
                                   zoom_range=0.2,
                                   horizontal_flip=True)

# Note that the validation data should not be augmented!
test_datagen = ImageDataGenerator(rescale=1.0/255.)

# Flow training images in batches of 20 using train_datagen generator
train_generator = train_datagen.flow_from_directory(train_dir,
                                                    batch_size=20,
                                                    class_mode='binary',
                                                    target_size=(150, 150))

# Flow validation images in batches of 20 using test_datagen generator
validation_generator = test_datagen.flow_from_directory(test_dir,
                                                        batch_size=20,
                                                        class_mode='binary',
                                                        target_size=(150, 150))

history = model.fit(
    train_generator,
    validation_data=validation_generator,
    steps_per_epoch=100,
    epochs=15,
    validation_steps=50,
    verbose=0)

# plotting graph
# -----------------------------------------------------------
# Retrieve a list of list results on training and test data
# sets for each training epoch
# -----------------------------------------------------------
acc = history.history['accuracy']
val_acc = history.history['val_accuracy']
loss = history.history['loss']
val_loss = history.history['val_loss']

epochs = range(len(acc))  # Get number of epochs

# ------------------------------------------------
# Plot training and validation accuracy per epoch
# ------------------------------------------------
plt.plot(epochs, acc)
plt.plot(epochs, val_acc)
plt.title('Training and validation accuracy')
plt.figure()

# ------------------------------------------------
# Plot training and validation loss per epoch
# ------------------------------------------------
plt.plot(epochs, loss)
plt.plot(epochs, val_loss)
plt.title('Training and validation loss')

print("\ntime taken to execute {}sec".format(
    (datetime.datetime.now() - then)//datetime.timedelta(seconds=1))
)

# plt.show()
