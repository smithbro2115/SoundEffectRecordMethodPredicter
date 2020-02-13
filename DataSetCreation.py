import pandas as pd
from sklearn.preprocessing import LabelEncoder
import numpy as np
import math
import os


def load_folder_of_excel_into_data_set(dir_path):
    names_and_methods = []
    for path in os.listdir(dir_path):
        full_path = f"{dir_path}\\{path}"
        if os.path.isfile(full_path) and os.path.splitext(full_path)[1] == ".xlsx":
            df = import_excel(full_path)
            names_and_methods += get_sfx_names_and_methods(df)
    save_names_and_methods_to_csv(names_and_methods)


def import_excel(path):
    data_frame = pd.read_excel(path)
    return data_frame


def get_sfx_names_and_methods(data_frame):
    names_and_methods = []
    data_frame = normalize_data_frame(data_frame)
    for row in data_frame.iterrows():
        name = str(row[1]["sfx name"])
        if name[:6] != "sound:":
            continue
        name = name[6:].strip()
        methods_used = get_methods_used_from_row(row)
        sound = [name] + get_method_columns_from_list(methods_used)
        names_and_methods.append(sound)
    return names_and_methods


def normalize_data_frame(data_frame):
    for column in data_frame.columns:
        try:
            data_frame[column] = data_frame[column].str.lower()
        except AttributeError:
            pass
    data_frame.columns = map(try_to_lowercase, data_frame.columns)
    return data_frame


def try_to_lowercase(value):
    try:
        return value.lower()
    except AttributeError:
        return value


def get_methods_used_from_row(row):
    methods_used = []
    for key, value in row[1].items():
        column_header = key
        try:
            if math.isnan(float(value)):
                continue
        except ValueError:
            pass
        try:
            if column_header.startswith('rec'):
                methods_used.append(0)
            elif column_header.startswith('foley'):
                methods_used.append(1)
            elif column_header.startswith('library'):
                methods_used.append(2)
        except AttributeError:
            continue
    return methods_used


def get_method_columns_from_list(methods_list):
    columns = []
    for i in range(3):
        if i in methods_list:
            columns.append(1)
        else:
            columns.append(0)
    return columns


def save_names_and_methods_to_csv(names_and_methods):
    data_frame = pd.DataFrame(names_and_methods, columns=['name', 'record', 'foley', 'library'])
    data_frame.to_csv("raw_data_set.csv", index=False)


class WordEncoder:
    def __init__(self):
        self.label_encoder = LabelEncoder()
        try:
            self.load_fit()
        except FileNotFoundError:
            pass

    def load_fit(self):
        self.label_encoder.classes_ = np.load('classes_.npy')

    def fit_label_encoder_from_words(self, csv_path, column):
        data_frame = pd.read_csv(csv_path)
        complete_word_list = []
        for row in data_frame[column]:
            row_word_list = row.split()
            for word in row_word_list:
                if word not in complete_word_list:
                    complete_word_list.append(word)
        self.label_encoder.fit(complete_word_list)
        self.save_word_list()
        self.save_fit()

    def save_word_list(self):
        name_mapping = list(zip(self.label_encoder.classes_, self.label_encoder.transform(self.label_encoder.classes_)))
        data_frame = pd.DataFrame(name_mapping, columns=['word', 'map'])
        data_frame.to_csv('word_list.csv', index=False)

    def save_fit(self):
        np.save("classes_.npy", self.label_encoder.classes_)

    def convert_to_one_hot(self, string):
        word_list = string.split()
        word_array = np.array(word_list)
        vec = self.label_encoder.transform(word_array)
        return " ".join([str(num) for num in vec])

    def convert_csv_column_to_one_hot(self, path, column):
        data_frame = pd.read_csv(path)
        data_frame[column] = data_frame[column].apply(self.convert_to_one_hot)
        return data_frame

    def decode_word_list(self, word_list):
        print(word_list)
        return self.label_encoder.inverse_transform(np.fromstring(word_list, dtype=int, sep=' '))


# load_folder_of_excel_into_data_set("C:\\Users\\Josh\\Documents\\SFX List Train Sheets")

# word_encoder = WordEncoder()
# word_encoder.fit_label_encoder_from_words("raw_data_set.csv", 'name')
# test_data = word_encoder.convert_csv_column_to_one_hot("raw_data_set.csv", "name")
# test_data.to_csv("data_set.csv", index=False)
# print(word_encoder.decode_word_list(test_data["name"][50]))
