
import matplotlib.pyplot as plt
import tensorflow as tf
import tensorflow_datasets as tfds
import tensorflow.keras as k

# check to see if loaded dataset is compatible with S3 API
rps_builder = tfds.builder("mnist:3.*.*")
print(rps_builder.version.implements(tfds.core.Experiment.S3))
print("\n")

# downloading and splitting data
train_ds, test_ds = tfds.load('mnist:3.*.*', split=['train', 'test'])
print(len(list(train_ds)))
print(len(list(test_ds)))
print("\n")

# combined set
combined = tfds.load('mnist:3.*.*', split='test+train')
print(len(list(combined)))
print("\n")

# first 10,000 set
first10k = tfds.load('mnist:3.*.*', split='train[:10000]')
print(len(list(first10k)))
print("\n")

# first 20% set
first20p = tfds.load('mnist:3.*.*', split='train[:20%]')
print(len(list(first20p)))
print("\n")

# composed split dataset
composed = tfds.load('mnist:3.*.*', split='train[-80%:]+test[:10%]')
print(len(list(composed)))
print("\n")

# composed dataset
val_ds = tfds.load('mnist:3.*.*', split=['train[{}%:{}%]'.format(k, k + 20)
                                         for k in range(0, 100, 20)])
train_ds = tfds.load('mnist:3.*.*', split=['train[:{}%] + train[{}%:]'.format(k, k + 20)
                                           for k in range(0, 100, 20)])
print(val_ds)
print(len(list(val_ds)))
print(len(list(train_ds)))
print("\n")
