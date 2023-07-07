import pathlib
import numpy as np
import tensorflow as tf
import tensorflow.keras as k

'''
interpreter gives us the ability to test our model using 
Python on our developer workstation so you don't need 
to deploy it to a mobile and embedded system before 
you can start using it
'''
# loading tflite model
interpreter = tf.lite.Interpreter(model_content=tflite_model)
# or $interpreter = tf.lite.Interpreter(model_path="converted_model.tflite")
interpreter.allocate_tensors()

# getting input and output tensors
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# point data to be used for testing interpreter
interpreter.set_tensor(input_details[0]['index'], input_data)
interpreter.invoke()
tflite_results = interpreter.get_tensor(output_details[0]['index'])

# plot input_data and tflite_results
