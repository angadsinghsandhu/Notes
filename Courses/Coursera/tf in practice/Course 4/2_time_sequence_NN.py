import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras

# writing helper functions to create time series


def plot_series(time, series, title='', format="-", start=0, end=None):
    plt.plot(time[start:end], series[start:end], format)
    plt.xlabel("Time")
    plt.ylabel("Value")
    plt.title(title)
    plt.grid(True)


def trend(time, slope=0):
    return slope * time


def seasonal_pattern(season_time):
    """Just an arbitrary pattern, you can change it if you wish"""
    return np.where(season_time < 0.4,
                    np.cos(season_time * 2 * np.pi),
                    1 / np.exp(3 * season_time))


def seasonality(time, period, amplitude=1, phase=0):
    """Repeats the same pattern at each period"""
    season_time = ((time + phase) % period) / period
    return amplitude * seasonal_pattern(season_time)


def noise(time, noise_level=1, seed=None):
    rnd = np.random.RandomState(seed)
    return rnd.randn(len(time)) * noise_level


# parameters of data
time = np.arange(4 * 365 + 1, dtype="float32")
baseline = 10
series = trend(time, 0.1)
baseline = 10
amplitude = 20
slope = 0.09
noise_level = 5

# Creating the series
series = baseline + trend(time, slope) + \
    seasonality(time, period=365, amplitude=amplitude)
# Updating with noise
series += noise(time, noise_level, seed=42)

# splitting data
split_time = 1000
time_train = time[:split_time]
x_train = series[:split_time]
time_valid = time[split_time:]
x_valid = series[split_time:]

window_size = 20
batch_size = 32
shuffle_buffer_size = 1000

plt.figure(figsize=(10, 6))
plot_series(time_valid, x_valid, "Initial Time Series")


def windowed_dataset(series, window_size, batch_size, shuffle_buffer):
    dataset = tf.data.Dataset.from_tensor_slices(series)
    dataset = dataset.window(window_size + 1, shift=1, drop_remainder=True)
    dataset = dataset.flat_map(lambda window: window.batch(window_size + 1))
    dataset = dataset.shuffle(shuffle_buffer).map(
        lambda window: (window[:-1], window[-1]))
    dataset = dataset.batch(batch_size).prefetch(1)
    return dataset


# creating windowed tensorflow dataset
dataset = windowed_dataset(
    x_train, window_size, batch_size, shuffle_buffer_size)

######################=======================#######################
######################========SIMPLE_NN======#######################
######################=======================#######################

# testing basic NN Model
print("\n\n")
model = tf.keras.models.Sequential([
    tf.keras.layers.Dense(10, input_shape=[window_size], activation="relu"),
    tf.keras.layers.Dense(10, activation="relu"),
    tf.keras.layers.Dense(1)
])

model.compile(loss="mse", optimizer=tf.keras.optimizers.SGD(
    lr=1e-6, momentum=0.9))
model.fit(dataset, epochs=100, verbose=1)

forecast = []
for time in range(len(series) - window_size):
    forecast.append(model.predict(series[time:time + window_size][np.newaxis]))

forecast = forecast[split_time-window_size:]
results = np.array(forecast)[:, 0, 0]


plt.figure(figsize=(10, 6))

txt = "prediction using simple NN"
plot_series(time_valid, x_valid, txt)
plot_series(time_valid, results, txt)
plt.show()

# printing Error
temp = tf.keras.metrics.mean_absolute_error(x_valid, results).numpy()
print("\nthe Mean Absolute Error of prediction using Simple NN is {}".format(temp))

######################=======================#######################
######################=OPTIMAL_LEARNING_RATE=#######################
######################=======================#######################

dataset = windowed_dataset(
    x_train, window_size, batch_size, shuffle_buffer_size)

print("\n\n")
model = tf.keras.models.Sequential([
    tf.keras.layers.Dense(10, input_shape=[window_size], activation="relu"),
    tf.keras.layers.Dense(10, activation="relu"),
    tf.keras.layers.Dense(1)
])

# Creating learning rate scheduler callback
lr_schedule = tf.keras.callbacks.LearningRateScheduler(
    lambda epoch: 1e-8 * 10 ** (epoch / 20))

optimizer = tf.keras.optimizers.SGD(lr=1e-8, momentum=0.9)
model.compile(loss="mse", optimizer=optimizer)
history = model.fit(dataset, epochs=100, callbacks=[lr_schedule], verbose=1)

# Plotting different learning rates with different loss and choosing out optimal rate
lrs = 1e-8 * (10 ** (np.arange(100) / 20))
plt.semilogx(lrs, history.history["loss"])
plt.axis([1e-8, 1e-3, 0, 300])
plt.title("Plotting different learning rates with different loss and choosing out optimal rate")
plt.show()

######################=========================#######################
######################=Simple_NN_with_Tuned_LR=#######################
######################=========================#######################

window_size = 30
dataset = windowed_dataset(
    x_train, window_size, batch_size, shuffle_buffer_size)

print("\n\n")
model = tf.keras.models.Sequential([
    tf.keras.layers.Dense(10, activation="relu", input_shape=[window_size]),
    tf.keras.layers.Dense(10, activation="relu"),
    tf.keras.layers.Dense(1)
])

optimizer = tf.keras.optimizers.SGD(lr=8e-6, momentum=0.9)
model.compile(loss="mse", optimizer=optimizer)
history = model.fit(dataset, epochs=500, verbose=1)

# plotting the loss as training progresses
loss = history.history['loss']
epochs = range(len(loss))
plt.plot(epochs, loss, 'b', label='Training Loss')
plt.title("plotting the loss as training progresses")
plt.show()

# Plot all but the first 10 iterations of training
loss = history.history['loss']
epochs = range(10, len(loss))
plot_loss = loss[10:]
print(plot_loss)
plt.plot(epochs, plot_loss, 'b', label='Training Loss')
plt.title("Plot all but the first 10 iterations of training")
plt.show()

# creating forecast
forecast = []
for time in range(len(series) - window_size):
    forecast.append(model.predict(series[time:time + window_size][np.newaxis]))

forecast = forecast[split_time-window_size:]
results = np.array(forecast)[:, 0, 0]


plt.figure(figsize=(10, 6))

txt = "Prediction using Simple NN with Tuned LR"
plot_series(time_valid, x_valid, txt)
plot_series(time_valid, results, txt)
plt.show()

# printing Error
temp = tf.keras.metrics.mean_absolute_error(x_valid, results).numpy()
print("\nthe Mean Absolute Error of prediction using Simple NN with lr tuning is {}".format(temp))
