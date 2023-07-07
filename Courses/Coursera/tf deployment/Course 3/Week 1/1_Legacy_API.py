
import matplotlib.pyplot as plt
import tensorflow as tf
import tensorflow_datasets as tfds
import tensorflow.keras as k

# merging with legacy api
total = tfds.Split.TRAIN + tfds.Split.TEST
ds = tfds.load("mnist", split=total)
print("MNIST Dataset Size : " + str(len(list(ds))) + "\n")

# using subsplit
s1, s2, s3, s4 = tfds.Split.TRAIN.subsplit(k=4)
for i in range(1, 5):
    string = "s" + str(i)
    split = eval(string)
    # calling split using '.load()'
    num = len(list(tfds.load("mnist", split=split)))
    print("data subsplit s{} size is : {}".format(
        i, num))
