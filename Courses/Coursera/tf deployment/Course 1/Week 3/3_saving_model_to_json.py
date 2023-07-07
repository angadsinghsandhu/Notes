import time
import h5py
import numpy as np
import tensorflow as tf
import tensorflow.keras as k
import tensorflowjs as tfjs

# creating and executing simple model
model = k.Sequential([k.layers.Dense(units=1, input_shape=[1])])
model.compile(optimizer='sgd', loss='mean_squared_error')

xs = np.array([-1, 0, 1, 2, 3, 4], dtype=int)
ys = np.array([-3, -1, 1, 3, 5, 7], dtype=int)

model.fit(xs, ys, epochs=100)
print(model.predict([10.0]))

# saving model as '.pb' file
# model.save('./')

# saving model as '.json' and '.bin' file
tfjs.converters.save_keras_model(model, "./")

# Save the entire model to a HDF5 file..
# model.save('my_model.h5')
