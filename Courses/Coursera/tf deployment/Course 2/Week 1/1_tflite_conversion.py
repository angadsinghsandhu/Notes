import pathlib
import numpy as np
import tensorflow as tf
import tensorflow.keras as k

'''
## methods of conversion of custom trained models into '.tflite' models
# SavedModel (preferred)
tf.lite.TFLiteConverter.from_saved_model(...)

# KerasSavedModel from '.h5' file
tf.lite.TFLiteConverter.from_keras_model(...)

# Concrete Functions
tf.lite.TFLiteConverter.from_concrete_functions(...)


## methods of conversion of pre-trained models from keras
pre_trained_model = k.applications.MobileNet()
tf.saved_model.save(pre_trained_model, "./tmp/saved_model/1")
'''


# example
# create model
model = k.Sequential([k.layers.Dense(units=1, input_shape=[1])])
model.compile(optimizer='sgd', loss='mean_squared_error')

xs = np.array([-1, 0, 1, 2, 3, 4], dtype=int)
ys = np.array([-3, -1, 1, 3, 5, 7], dtype=int)

model.fit(xs, ys, epochs=100)
print(model.predict([10.0]))

# export saved model
export_dir = './tmp/saved_model'
tf.saved_model.save(model, export_dir)

'''
using post -raining quantization to reduce '.tflite' file 
size i.e. converting all weights of model from floats to ints

#creating yield generator
def generator():
    data = tfjs.load(...)
    for _ in range(num_calibration_steps):
        image, = data.take(1)
        yeild[image]

# passing representative dataset into converter
converter.representative_dataset = tf.lite.RepresentativeDataset(generator)

here the genrator is a representative dataset which is used for evaluating 
best possible optimization by recording dynamic ranges, this is done by running
multiple infrences on a floating point TensorFlow Model using this dataset as input
the values logged from this can help determine the scaling parameters needed to
execute all tensors of the model in integer arithmatic
hence, quantizing activations along with weights

some ops dont have a quantized implementation and fall back to float
but special purpose acceleratos only use integer values. Hence, 
this can be solved by constraining the quantization target specification
to TFLite's 'INT8' built-in ops

# restricting ti int8
converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]
'''

# converting model
converter = tf.lite.TFLiteConverter.from_saved_model(export_dir)
converter.optimizations = [tf.lite.Optimize.OPTIMIZE_FOR_LATENCY]
tflite_model = converter.convert()

'''
tf-select helps to keep the part of the model which are 
supported by Ops and hence convertable to tflite format

# using tf select
converter.target_ops = [tf.lite.OpsSet.TFLITE_BUILTINS,
                        tf.lite.OpsSet.SELECT_TF_OPS]
tflite_model = converter.convert()
'''

# saving converted model
tflite_model_file = pathlib.Path('./tmp/foo.tflite')
tflite_model_file.write_bytes(tflite_model)
