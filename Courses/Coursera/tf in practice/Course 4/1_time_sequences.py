import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras


# setting up the time series with seasonality, trend and a bit of noise.
def plot_series(time, series, title="", format="-", start=0, end=None):
    plt.plot(time[start:end], series[start:end], format)
    plt.xlabel("Time")
    plt.ylabel("Value")
    plt.title(title)
    plt.grid(True)
    plt.show()


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


time = np.arange(4 * 365 + 1, dtype="float32")
baseline = 10
series = trend(time, 0.1)
amplitude = 40
slope = 0.05
noise_level = 5

# Create the series
series = baseline + trend(time, slope) + \
    seasonality(time, period=365, amplitude=amplitude)
# Update with noise
series += noise(time, noise_level, seed=42)

plt.figure(figsize=(10, 6))
plot_series(time, series, "initial Time-series")

# Now that we have the time series, let's split it so we can start forecasting
split_time = 1000
time_train = time[:split_time]
x_train = series[:split_time]
time_valid = time[split_time:]
x_valid = series[split_time:]
plt.figure(figsize=(10, 6))
plot_series(time_train, x_train, "train set forecasting")

plt.figure(figsize=(10, 6))
plot_series(time_valid, x_valid, "validation set forecasting")

# taking the naitive forecast
naive_forecast = series[split_time - 1:-1]

plt.figure(figsize=(10, 6))
plot_series(time_valid, x_valid, "validation set forecast")
plot_series(time_valid, naive_forecast, "validation set naitive forecast")

# zooming in on validation period
plt.figure(figsize=(10, 6))
plot_series(time_valid, x_valid,
            "zoomed-in validation set forecasting", start=0, end=150)
plot_series(time_valid, naive_forecast,
            "zoomed-in validation set naitive forecasting", start=1, end=151)

# We can see that the naive forecast lags 1 step behind the time series.

# computing the mean squared error and
# the mean absolute error
# between the forecasts and the predictions in the validation period:
print('\n\n== validation set naitive forecasting ==\nMSE Value : ')
print(keras.metrics.mean_squared_error(x_valid, naive_forecast).numpy())
print('\nMAE Value : ')
print(keras.metrics.mean_absolute_error(x_valid, naive_forecast).numpy())
# this is our baseline

# using moving averages


def moving_average_forecast(series, window_size):
    """Forecasts the mean of the last few values.
       If window_size=1, then this is equivalent to naive forecast"""
    forecast = []
    for time in range(len(series) - window_size):
        forecast.append(series[time:time + window_size].mean())
    return np.array(forecast)


moving_avg = moving_average_forecast(series, 30)[split_time - 30:]

plt.figure(figsize=(10, 6))
plot_series(time_valid, x_valid, "validation set forecast")
plot_series(time_valid, moving_avg,
            "validation set with moving-averages forecast")
plt.show()

print('\n\n== validation set with moving averages forecast ==\nMSE Value : ')
print(keras.metrics.mean_squared_error(x_valid, moving_avg).numpy())
print('\nMAE Value : ')
print(keras.metrics.mean_absolute_error(x_valid, moving_avg).numpy())
# That's worse than naive forecast!
# The moving average does not anticipate trend or seasonality,
# so let's try to remove them by using differencing.

# Since the seasonality period is 365 days,
# we will subtract the value at time t – 365 from the value at time t.
diff_series = (series[365:] - series[:-365])
diff_time = time[365:]

plt.figure(figsize=(10, 6))
plot_series(diff_time, diff_series, "Time-Series with Differencing")
plt.show()

# now using moving average after trend and seasonality are gone
diff_moving_avg = moving_average_forecast(
    diff_series, 50)[split_time - 365 - 50:]

plt.figure(figsize=(10, 6))
plot_series(
    time_valid, diff_series[split_time - 365:], "validation set forecast with differencing")
plot_series(time_valid, diff_moving_avg,
            "validation set forecast with differencing and moving-averages")
plt.show()

# Now let's bring back the trend and seasonality by adding the past values from t – 365:
diff_moving_avg_plus_past = series[split_time - 365:-365] + diff_moving_avg

plt.figure(figsize=(10, 6))
plot_series(time_valid, x_valid,
            "initial validation set forecast")
plot_series(time_valid, diff_moving_avg_plus_past,
            "validation set forecast with differencing and moving-averages with trend and seasonality added back")
plt.show()

print('\n\n== validation set forecast with differencing and moving-averages with trend and seasonality added back ==\nMSE Value : ')
print(keras.metrics.mean_squared_error(
    x_valid, diff_moving_avg_plus_past).numpy())
print('\nMAE Value : ')
print(keras.metrics.mean_absolute_error(
    x_valid, diff_moving_avg_plus_past).numpy())
# Better than naive forecast, good.
# However the forecasts look a bit too random,
#  because we're just adding past values, which were noisy.

#  Let's use a moving averaging on past values to remove some of the noise:
diff_moving_avg_plus_smooth_past = moving_average_forecast(
    series[split_time - 370:-360], 10) + diff_moving_avg

plt.figure(figsize=(10, 6))
plot_series(time_valid, x_valid,
            "initial validation set forecast")
plot_series(time_valid, diff_moving_avg_plus_smooth_past,
            "validation set forecast with moving averaging on past values to remove some of the noise")
plt.show()

print('\n\n== validation set forecast with moving averaging on past values to remove some of the noise ==\nMSE Value : ')
print(keras.metrics.mean_squared_error(
    x_valid, diff_moving_avg_plus_smooth_past).numpy())
print('\nMAE Value : ')
print(keras.metrics.mean_absolute_error(
    x_valid, diff_moving_avg_plus_smooth_past).numpy())
