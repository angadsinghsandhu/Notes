import tensorflow as tf
import tensorflow.keras as k
import tensorflow_datasets as tfds
import multiprocessing


def argment(features):  # transformation set
    X = tf.image.random_flip_left_right(features['image'])
    X = tf.image.random_flip_up_down(X)
    X = tf.image.random_brightness(X, max_delta=0.1)
    X = tf.image.random_saturation(X, lower=0.75, upper=1.5)
    X = tf.image.random_hue(X, max_delta=0.1)
    X = tf.image.random_contrast(X, lower=0.75, upper=1.5)
    X = tf.image.resize_images(X, (224, 224))
    image = X / 255.0
    return image, features['label']


# loading dataset
dataset = tfds.load('cats_vs_dogs', split=tfds.Split.TRAIN)

# dynamic autotune func
autotune = tf.data.experimental.AUTOTUNE

# getting number of available cores
num_cores = multiprocessing.cpu_count()

# mapping transformation set parallely
tf.data.Dataset.map(argment, num_parallel_calls=autotune)

# prefetch to use cpu while using gpu
tf.data.Dataset.prefetch(dataset, buffer_size=autotune)

# parallel data extraction
TFRECORDS_DIR = '/root/tensorflow_datasets/cats_vs_dogs/<dataset-version>/'
files = tf.data.Dataset.list_files(TFRECORDS_DIR +
                                   "cats_vs_dogs-train.tfrecord-*")

num_parallel_reads = 4

tf.data.Dataset.interleave(tf.data.TFRecordDataset,
                           cycle_length=num_parallel_reads,
                           num_parallel_calls=autotune)


###===BEST_PRACTICES===###

'''
MAP TRANSFORMATION => SOLUTION: VECTORIZING

When vectorizing, we'll have map operate over a batch 
of inputs at the same time instead of one by one. There 
are two ways that you can achieve this. 

First, of course is just to define a batch by specifying 
a batch with a DOT batch method and then mapping that. 

$   dataset = dataset.batch(BATCH_SIZE).map(func)


The second is to use 
an options object and on set map vectorization to be enabled

$    options = tf.data.Options()
$    options.experimental_optimization.map_vectorization.enabled = True
$    dataset = dataset.with_options(options)
'''

'''
MAP & CACHE => SOLUTION: MAP Then CACHE

a scenario where your data needs a 
lot of transformations in that case 
you'll end up with a user-defined function
that's quite expensive in operation. 
So it's recommended that you apply the
cash transform after the map transformation.
This is done to avoid going through performing 
the computationally costly transformation repeatedly.

$    transformed_dataset = dataset.map(transforms).cache()
'''

'''
SHUFFLE & REPEAT => SOLUTION: (Order Selection)

 the repeat transformation repeats the input data and 
 number of times. Whereas Shuffle randomizes the order 
 of the datasets examples when the repeat transformation 
 is applied. Before the shuffle transformation the epoch 
 boundaries can be blurred that is some elements can be 
 repeated before others even appear once. On the other 
 hand if the shuffle transformation is applied before the 
 repeat transformation, then performance might slow down 
 at the beginning of each Epoch, related to the initialization 
 of the internal state of the shuffle transformation.

$   #for order guarantee
$   .shuffle().repeat()

$   #for better performance
$   .repeat().shuffle()
'''
