
import numpy as np
import pandas as pd
import tensorflow as tf
import tensorflow.keras as k

# creating dataframe from pandas
URL = 'https://storage.googleapis.com/applied-dl/heart.csv'
df = pd.read_csv(URL)
df.head()

# spliting data
data_len = df.shape[0]
split_ratio = 0.8
validation_split_ratio = 0.8

train_len = int(round(data_len * split_ratio))
val_len = int(round(train_len * validation_split_ratio))

train, test = df.iloc[:train_len], df.iloc[train_len:]
train, val = train.iloc[:val_len], train.iloc[val_len:]

print("\n\n\ntrain shape : {}".format(train.shape))
print("test shape : {}".format(test.shape))
print("val shape : {}\n\n\n".format(val.shape))

# creating input pipeline
# A utility method to create a tf.data dataset from a Pandas Dataframe
# not taking into account if dataset dosent fit into memory,
# then we directly load it from memory


def df_to_dataset(dataframe, shuffle=True, batch_size=32):
    dataframe = dataframe.copy()
    labels = dataframe.pop('target')
    ds = tf.data.Dataset.from_tensor_slices((dict(dataframe), labels))
    if shuffle:
        ds = ds.shuffle(buffer_size=len(dataframe))
    ds = ds.batch(batch_size)
    return ds


batch_size = 5
train_ds = df_to_dataset(train, batch_size=batch_size)
test_ds = df_to_dataset(test, shuffle=True, batch_size=batch_size)
val_ds = df_to_dataset(val, shuffle=True, batch_size=batch_size)

# checking format of data
for feature_batch, label_batch in train_ds.take(1):
    print('\n\n')
    print('Every feature:', list(feature_batch.keys()))
    print('\n\n')
    print('A batch of ages:', feature_batch['age'])
    print('\n\n')
    print('A batch of targets:', label_batch)
    print('\n\n')

# creating Feature Columns
# We will use this batch to demonstrate several types of feature columns
example_batch = next(iter(train_ds))[0]

# A utility method to create a feature column
# and to transform a batch of data


def demo(feature_column):
    feature_layer = k.layers.DenseFeatures(feature_column, dtype='float64')
    print("\n\n\n\n")
    print(feature_layer(example_batch).numpy())


# Numeric Column => simplest version of feature column
age = tf.feature_column.numeric_column("age")
demo(age)

# Bucketized Columns are where categories are based on numerical ranges
age_buckets = tf.feature_column.bucketized_column(
    age, boundaries=[18, 25, 30, 35, 40, 45, 50, 55, 60, 65])
demo(age_buckets)

# Categorical Columns, mapping strigs to numeric values
thal = tf.feature_column.categorical_column_with_vocabulary_list(
    'thal', ['fixed', 'normal', 'reversible'])

thal_one_hot = tf.feature_column.indicator_column(thal)
demo(thal_one_hot)

# Embedding Columns, this ia a categorical column for large number of strings
# Notice the input to the embedding column is the categorical column
# we previously created
thal_embedding = tf.feature_column.embedding_column(thal, dimension=8)
demo(thal_embedding)

# Hashed Feature Columns, calculating a hash value of the input,
# then encoding a string
thal_hashed = tf.feature_column.categorical_column_with_hash_bucket(
    'thal', hash_bucket_size=10)
demo(tf.feature_column.indicator_column(thal_hashed))

# Crossed Feature Columns, combining multiple features
# into a single feature, better known as feature crosses
crossed_feature = tf.feature_column.crossed_column(
    [age_buckets, thal], hash_bucket_size=10)
FIXME(OverflowError: Python int too large to convert to C long)
# demo(tf.feature_column.indicator_column(crossed_feature))


###========CREATING AND IMPLEMENTING A MODEL========###


# choosing which colums to use
feature_columns = []

# numeric cols
for header in ['age', 'trestbps', 'chol', 'thalach', 'oldpeak', 'slope', 'ca']:
    feature_columns.append(tf.feature_column.numeric_column(header))
print("\n\n feature_columns : {}".format(feature_columns))

# bucketized cols
age_buckets = tf.feature_column.bucketized_column(
    age, boundaries=[18, 25, 30, 35, 40, 45, 50, 55, 60, 65])
feature_columns.append(age_buckets)

# indicator cols
thal = tf.feature_column.categorical_column_with_vocabulary_list(
    'thal', ['fixed', 'normal', 'reversible'])
thal_one_hot = tf.feature_column.indicator_column(thal)
feature_columns.append(thal_one_hot)

# embedding cols
thal_embedding = tf.feature_column.embedding_column(thal, dimension=8)
feature_columns.append(thal_embedding)

# crossed cols
crossed_feature = tf.feature_column.crossed_column(
    [age_buckets, thal], hash_bucket_size=10)
crossed_feature = tf.feature_column.indicator_column(crossed_feature)
feature_columns.append(crossed_feature)

# creating a feature layer
feature_layer = k.layers.DenseFeatures(feature_columns)

batch_size = 32
train_ds = df_to_dataset(train, batch_size=batch_size)
val_ds = df_to_dataset(val, shuffle=False, batch_size=batch_size)
test_ds = df_to_dataset(test, shuffle=False, batch_size=batch_size)

# Create, Compile, Train Model
model = tf.keras.Sequential([
    feature_layer,
    k.layers.Dense(128, activation='relu'),
    k.layers.Dense(128, activation='relu'),
    k.layers.Dense(1, activation='sigmoid')
])

model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])

model.fit(train_ds,
          validation_data=val_ds,
          epochs=5)

loss, accuracy = model.evaluate(test_ds)
print("Accuracy", accuracy)
