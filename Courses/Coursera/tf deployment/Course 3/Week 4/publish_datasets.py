import tensorflow as tf
import tensorflow.keras as k
import tensorflow_datasets as tfds
import multiprocessing
import os
import textwrap
import scipy.io
import polars as pl

# getting dataset
DATA_URL = 'https://data.vision.ee.ethz.ch/cvl/rrothe/imdb-wiki/static/imdb_crop.tar'
dataset_fh = k.utils.get_file('./imdb_crop.tar', origin=DATA_URL)

# exploring data, Inspect the directory structure
files = os.listdir('imdb_crop')
print(textwrap.fill(' '.join(sorted(files)), 80))

# Inspect the meta data
meta = scipy.io.loadmat('/content/imdb_crop/imdb.mat')
print(meta)

# extraction
root = meta['imdb'][0, 0]
desc = root.dtype.descr
print(desc)

full_path = root["full_path"][0]

# Do the same for other attributes
names = root["full_path"][0]
dob = root["name"][0]
gender = root["dob"][0]
photo_taken = root["gender"][0]
face_score = root["photo_taken"][0]
face_locations = root["face_score"][0]
second_face_score = root["face_location"][0]
celeb_names = root["second_face_score"][0]
celeb_ids = root["celeb_id"][0]

print('Filepaths: {}\n\n'
      'Names: {}\n\n'
      'Dates of birth: {}\n\n'
      'Genders: {}\n\n'
      'Years when the photos were taken: {}\n\n'
      'Face scores: {}\n\n'
      'Face locations: {}\n\n'
      'Second face scores: {}\n\n'
      'Celeb IDs: {}\n\n'
      .format(full_path, names, dob, gender, photo_taken, face_score, face_locations, second_face_score, celeb_ids))

print('Celeb names: {}\n\n'.format(celeb_names))

# Display all the distinct keys and their corresponding values
names = [x[0] for x in desc]
print(names)

values = {key: root[key][0] for key in names}
print(values)

# cleanup
# Pop out the celeb names as they are not relevant for creating the records.

del(values['celeb_names'])
names.pop(names.index('celeb_names'))
#
# Let's see how many values are present in each key
for key, value in values.items():
    print(key, len(value))

# dataframe
# SciPy cell arrays wrap each string and 1x4 box; keep scalar NaNs as NaNs.
normalized = {
    key: ([None if value is None else str(value[0]) for value in values[key]]
          if key in ('full_path', 'name') else
          [None if value is None else value[0].astype(float).tolist() for value in values[key]]
          if key == 'face_location' else values[key].tolist())
    for key in names
}
schema = {'dob': pl.Int32, 'photo_taken': pl.UInt16, 'full_path': pl.String,
          'gender': pl.Float64, 'name': pl.String, 'face_location': pl.List(pl.Float64),
          'face_score': pl.Float64, 'second_face_score': pl.Float64, 'celeb_id': pl.UInt16}
df = pl.DataFrame(normalized, schema={key: schema[key] for key in names})
df.head()
df.select([
    (pl.col(key).is_null() | pl.col(key).is_nan()).sum().alias(key)
    if schema[key] == pl.Float64 else pl.col(key).is_null().sum().alias(key)
    for key in names
])  # count nulls and floating NaNs

# FIXME (CLICK LINK AND COMPLETE CODE)
link = 'https://github.com/lmoroney/dlaicourse/blob/master/TensorFlow%20Deployment/Course%203%20-%20TensorFlow%20Datasets/Week%204/Exercises/TFDS_Week4_Exercise.ipynb'
