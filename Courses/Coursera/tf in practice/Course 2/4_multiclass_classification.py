import os
import datetime
import numpy as np
import tensorflow as tf
from tensorflow import keras as k
from matplotlib import pyplot as plt
from keras.preprocessing.image import ImageDataGenerator
from keras.preprocessing import image

# downloaded and unzipped Rock-paper-sciscors dataset from
# "http://www.laurencemoroney.com/rock-paper-scissors-dataset/"
# already in directory

# starting time
then = datetime.datetime.now()


class MyCallback(tf.keras.callbacks.Callback):  # creating callback class
    def on_epoch_end(self, epoch, logs={}):
        if (logs.get('accuracy') > 0.99):
            print("accuracy exceeded 99%...Stopping Training...")
            self.model.stop_training = True


        # instantiating callback
callbacks = MyCallback()

# defining directories
base_dir = f'D:/Code/AI/datasets/rock_paper_scissor'
train_dir = os.path.join(base_dir, 'train')
test_dir = os.path.join(base_dir, 'validation')

# defining train directories
train_rock_dir = os.path.join(train_dir, 'rock')
train_paper_dir = os.path.join(train_dir, 'paper')
train_scissors_dir = os.path.join(train_dir, 'scissors')

# defining test directories
test_rock_dir = os.path.join(test_dir, 'rock')
test_paper_dir = os.path.join(test_dir, 'paper')
test_scissors_dir = os.path.join(test_dir, 'scissors')

# file names
fh_train_rock = os.listdir(train_rock_dir)
fh_train_paper = os.listdir(train_paper_dir)
fh_train_scissors = os.listdir(train_scissors_dir)

# list names
print("\n\n")
print(fh_train_rock[:10])
print(fh_train_paper[:10])
print(fh_train_scissors[:10])

# number of images
print("\n")
print("cats test set : " + str(len(train_rock_dir)) + " images\n")
print("cats test set : " + str(len(train_paper_dir)) + " images\n")
print("cats test set : " + str(len(train_scissors_dir)) + " images\n")
print("cats test set : " + str(len(test_rock_dir)) + " images\n")
print("cats test set : " + str(len(test_paper_dir)) + " images\n")
print("cats test set : " + str(len(test_scissors_dir)) + " images\n")

# creating NN Model
model = tf.keras.models.Sequential([
    # Note the input shape is the desired size of the image 150x150 with 3 bytes color
    # This is the first convolution
    tf.keras.layers.Conv2D(64, (3, 3), activation='relu',
                           input_shape=(150, 150, 3)),
    tf.keras.layers.MaxPooling2D(2, 2),
    # The second convolution
    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2, 2),
    # The third convolution
    tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2, 2),
    # The fourth convolution
    tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2, 2),
    # Flatten the results to feed into a DNN
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dropout(0.5),
    # 512 neuron hidden layer
    tf.keras.layers.Dense(512, activation='relu'),
    tf.keras.layers.Dense(3, activation='softmax')
])

# printing model summary
print("Model Summary : \n")
model.summary()

# compile code
model.compile(loss='categorical_crossentropy',
              optimizer=k.optimizers.RMSprop(lr=0.001), metrics=['accuracy'])

# train_datagen = ImageDataGenerator(
#     rescale=1 / 255,
#     # also adding Data Augmentation
#     rotation_range=40,
#     width_shift_range=0.2,
#     height_shift_range=0.2,
#     shear_range=0.2,
#     zoom_range=0.2,
#     horizontal_flip=True,
#     fill_mode='nearest'
# )
# test_datagen = ImageDataGenerator(rescale=1/255)

# train_generator = train_datagen.flow_from_directory(
#     train_dir,
#     target_size=(150, 150),
#     batch_size=50,
#     class_mode='categorical'
# )

# test_generator = train_datagen.flow_from_directory(
#     test_dir,
#     target_size=(150, 150),
#     batch_size=50,
#     class_mode='categorical'
# )

TRAINING_DIR = f"D:/Code/AI/datasets/rock_paper_scissor/train/"
training_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=40,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest')

VALIDATION_DIR = f"D:/Code/AI/datasets/rock_paper_scissor/validation/"
validation_datagen = ImageDataGenerator(rescale=1./255)

train_generator = training_datagen.flow_from_directory(
    TRAINING_DIR,
    target_size=(150, 150),
    class_mode='categorical',
    batch_size=25
)

validation_generator = validation_datagen.flow_from_directory(
    VALIDATION_DIR,
    target_size=(150, 150),
    class_mode='categorical',
    batch_size=25
)

# training
history = model.fit(
    train_generator,
    steps_per_epoch=100,
    epochs=6,
    verbose=1,
    callbacks=[callbacks],
    # validation_data=test_generator,
    validation_data=validation_generator,
    validation_steps=10
)

# evaluating model
print('\nTest Data : \n')
# predicting images
path = 'D:/Code/AI/datasets/rock_paper_scissor/examples/rock1.png'
img = image.load_img(path, target_size=(150, 150))
x = image.img_to_array(img)
x = np.expand_dims(x, axis=0)

images = np.vstack([x])
classes = model.predict(images, batch_size=10)
print(classes)
if classes[0][0] == 1:
    print("this is a paper")
elif classes[0][1] == 1:
    print("this is a rock")
else:
    print("this is a scissors")

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
