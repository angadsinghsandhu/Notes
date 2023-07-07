import os
import datetime
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow import keras as k
from matplotlib import pyplot as plt
# from keras.optimizers import RMSprop
# from keras.optimizers import RMSprop
# from keras.optimizers import RMSprop
from keras.preprocessing.image import ImageDataGenerator
from keras.preprocessing import image

# starting time
then = datetime.datetime.now()

# creating callback class


class MyCallback(tf.keras.callbacks.Callback):
    def on_epoch_end(self, epoch, logs={}):
        if (logs.get('accuracy') > 0.99):
            print("accuracy exceeded 99%...Stopping Training...")
            self.model.stop_training = True


# instantiating callback
callbacks = MyCallback()

# downloaded and unzipped file from
# "https://storage.googleapis.com/mledu-datasets/cats_and_dogs_filtered.zip"
# already in directory

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
print("\n\n\n\n")
print(fh_train_cats[:10])
print(fh_train_dogs[:10])

# number of images
print("\n")
print("cats test set : " + str(len(train_cats_dir)) + " images\n")
print("cats test set : " + str(len(train_dogs_dir)) + " images\n")
print("cats test set : " + str(len(test_cats_dir)) + " images\n")
print("cats test set : " + str(len(test_dogs_dir)) + " images\n")

# creating NN Model
model = k.models.Sequential([
    k.layers.Conv2D(16, (3, 3), activation='relu', input_shape=(300, 300, 3)),
    k.layers.MaxPooling2D(2, 2),
    k.layers.Conv2D(32, (3, 3), activation='relu'),
    k.layers.MaxPooling2D(2, 2),
    k.layers.Conv2D(64, (3, 3), activation='relu'),
    k.layers.MaxPooling2D(2, 2),
    k.layers.Flatten(),
    k.layers.Dense(512, activation='relu'),
    k.layers.Dense(1, activation='sigmoid')
])

# printing model summary
print("Model Summary : \n")
model.summary()

# compile code
model.compile(loss='binary_crossentropy',
              optimizer=k.optimizers.RMSprop(lr=0.001), metrics=['accuracy'])

# preprocessing and rescaling using generators
train_datagen = ImageDataGenerator(
    rescale=1 / 255,
    # also adding Data Augmentation
    rotation_range=40,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest'
)
test_datagen = ImageDataGenerator(rescale=1/255)

train_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size=(300, 300),
    batch_size=20,
    class_mode='binary'
)

test_generator = train_datagen.flow_from_directory(
    test_dir,
    target_size=(300, 300),
    batch_size=20,
    class_mode='binary'
)

# training
history = model.fit(
    train_generator,
    steps_per_epoch=100,
    epochs=15,
    verbose=1,
    callbacks=[callbacks],
    validation_data=test_generator,
    validation_steps=10
)

# evaluating model
print('\nTest Data : \n')
# predicting images
path = 'D:/Code/AI/datasets/cats_and_dogs_filtered/examples/cat1.jpg'
img = image.load_img(path, target_size=(300, 300))
x = image.img_to_array(img)
x = np.expand_dims(x, axis=0)

images = np.vstack([x])
classes = model.predict(images, batch_size=10)
print(classes[0])
if classes[0] > 0.5:
    print("this is a dog")
else:
    print("this is a cat")

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
