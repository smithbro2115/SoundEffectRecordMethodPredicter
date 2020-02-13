import tensorflow as tf
from DataSetCreation import WordEncoder
import pandas as pd
import numpy as np


word_encoder = WordEncoder()
data_frame = pd.read_csv("data_set.csv")
# data_frame['name'] = data_frame['name'].apply(word_encoder.decode_word_list)
train_data, train_labels = tf.data.Dataset.from_tensor_slices(
    (data_frame['name'].values, data_frame['record'].values))

print(train_data, train_labels)
