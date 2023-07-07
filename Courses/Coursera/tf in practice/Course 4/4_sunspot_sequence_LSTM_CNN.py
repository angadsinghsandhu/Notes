import csv
import matplotlib.image as mpimg
import matplotlib.image as mpimg
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras

# this data set is downloaded from
# https://storage.googleapis.com/laurencemoroney-blog.appspot.com/Sunspots.csv

# helper function


def plot_series(time, series, title='', format="-", start=0, end=None):
    plt.plot(time[start:end], series[start:end], format)
    plt.xlabel("Time")
    plt.title(title)
    plt.ylabel("Value")
    plt.grid(True)


# initialize lists
time_step = []
sunspots = []

# open data set and add it to lists in memory
with open('D:/Code/AI/datasets/sunspots/sunspots.csv') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    next(reader)
    for row in reader:
        sunspots.append(float(row[2]))
        time_step.append(int(row[0]))

series = np.array(sunspots)
time = np.array(time_step)
plt.figure(figsize=(10, 6))
plot_series(time, series, "initial dataset")
plt.show()

split_time = 3000
time_train = time[:split_time]
x_train = series[:split_time]
time_valid = time[split_time:]
x_valid = series[split_time:]

window_size = 30
batch_size = 32
shuffle_buffer_size = 1000


def windowed_dataset(series, window_size, batch_size, shuffle_buffer):
    series = tf.expand_dims(series, axis=-1)
    ds = tf.data.Dataset.from_tensor_slices(series)
    ds = ds.window(window_size + 1, shift=1, drop_remainder=True)
    ds = ds.flat_map(lambda w: w.batch(window_size + 1))
    ds = ds.shuffle(shuffle_buffer)
    ds = ds.map(lambda w: (w[:-1], w[1:]))
    return ds.batch(batch_size).prefetch(1)


def model_forecast(model, series, window_size):
    ds = tf.data.Dataset.from_tensor_slices(series)
    ds = ds.window(window_size, shift=1, drop_remainder=True)
    ds = ds.flat_map(lambda w: w.batch(window_size))
    ds = ds.batch(32).prefetch(1)
    forecast = model.predict(ds)
    return forecast

######################=======================#######################
######################=OPTIMAL_LEARNING_RATE=#######################
######################=======================#######################


tf.keras.backend.clear_session()
tf.random.set_seed(51)
np.random.seed(51)
window_size = 64
batch_size = 256
train_set = windowed_dataset(
    x_train, window_size, batch_size, shuffle_buffer_size)
print(train_set)
print(x_train.shape)

print("\n\n")
model = tf.keras.models.Sequential([
    tf.keras.layers.Conv1D(filters=32, kernel_size=5,
                           strides=1, padding="causal",
                           activation="relu",
                           input_shape=[None, 1]),
    tf.keras.layers.LSTM(64, return_sequences=True),
    tf.keras.layers.LSTM(64, return_sequences=True),
    tf.keras.layers.Dense(30, activation="relu"),
    tf.keras.layers.Dense(10, activation="relu"),
    tf.keras.layers.Dense(1),
    tf.keras.layers.Lambda(lambda x: x * 400)
])

# Creating learning rate scheduler callback
lr_schedule = tf.keras.callbacks.LearningRateScheduler(
    lambda epoch: 1e-8 * 10 ** (epoch / 20))

optimizer = tf.keras.optimizers.SGD(lr=1e-8, momentum=0.9)
model.compile(loss=tf.keras.losses.Huber(),
              optimizer=optimizer,
              metrics=["mae"])
history = model.fit(train_set, epochs=100, callbacks=[lr_schedule])

# Plotting different learning rates with different loss and choosing out optimal rate
plt.semilogx(history.history["lr"], history.history["loss"])
plt.title("Plotting different learning rates with different loss and choosing out optimal rate")
plt.axis([1e-8, 1e-4, 0, 60])
plt.show()

######################========================================#######################
######################=TRAINING_BIDIRECTIONAL_LSTM_and_1DConv=#######################
######################========================================#######################

tf.keras.backend.clear_session()
tf.random.set_seed(51)
np.random.seed(51)

train_set = windowed_dataset(
    x_train, window_size=60, batch_size=100, shuffle_buffer=shuffle_buffer_size)

print("\n\n")
model = tf.keras.models.Sequential([
    tf.keras.layers.Conv1D(filters=60, kernel_size=5,
                           strides=1, padding="causal",
                           activation="relu",
                           input_shape=[None, 1]),
    tf.keras.layers.LSTM(60, return_sequences=True),
    tf.keras.layers.LSTM(60, return_sequences=True),
    tf.keras.layers.Dense(30, activation="relu"),
    tf.keras.layers.Dense(10, activation="relu"),
    tf.keras.layers.Dense(1),
    tf.keras.layers.Lambda(lambda x: x * 400)
])


optimizer = tf.keras.optimizers.SGD(lr=1e-5, momentum=0.9)
model.compile(loss=tf.keras.losses.Huber(),
              optimizer=optimizer,
              metrics=["mae"])
history = model.fit(train_set, epochs=500)

# creating forecast
rnn_forecast = model_forecast(model, series[..., np.newaxis], window_size)
rnn_forecast = rnn_forecast[split_time - window_size:-1, -1, 0]

plt.figure(figsize=(10, 6))
plot_series(time_valid, x_valid)
plot_series(time_valid, rnn_forecast, "Bidirectional LSTM Prediction")
plt.show()

# printing Error
temp = tf.keras.metrics.mean_absolute_error(x_valid, rnn_forecast).numpy()
print("\nthe Mean Absolute Error of prediction using Bidirectional LSTM Prediction is {}".format(temp))

# -----------------------------------------------------------
# Retrieve a list of list results on training and test data
# sets for each training epoch
# -----------------------------------------------------------

loss = history.history['loss']
epochs = range(len(loss))  # Get number of epochs

# ------------------------------------------------
# Plot training and validation loss per epoch
# ------------------------------------------------
plt.plot(epochs, loss, 'r')
plt.title('Training loss')
plt.xlabel("Epochs")
plt.ylabel("Loss")
plt.legend(["Loss"])
plt.figure()
plt.show()

# ------------------------------------------------
# Plot training and validation loss per epoch
# ------------------------------------------------
zoomed_loss = loss[200:]
zoomed_epochs = range(200, 500)

plt.plot(zoomed_epochs, zoomed_loss, 'r')
plt.title('Zoomed Training loss')
plt.xlabel("Epochs")
plt.ylabel("Loss")
plt.legend(["Loss"])
plt.figure()
plt.show()

print("\n\nThe RNN forecast list is:\n")
print(rnn_forecast)
