import pandas as pd
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
        name = name[7:]
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
    data_frame.to_csv("data_set.csv", index=False)

