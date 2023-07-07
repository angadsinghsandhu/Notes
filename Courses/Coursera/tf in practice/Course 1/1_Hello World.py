import numpy as np
import tensorflow as tf
from tensorflow import keras as k

model = k.Sequential([k.layers.Dense(units=1, input_shape=[1])])
model.compile(optimizer='sgd', loss='mean_squared_error')

xs = np.array([-1, 0, 1, 2, 3, 4], dtype=int)
ys = np.array([-3, -1, 1, 3, 5, 7], dtype=int)

model.fit(xs, ys, epochs=100)
print(model.predict([10.0]))
