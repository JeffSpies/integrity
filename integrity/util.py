import fnmatch
import glob
import pymongo
import yaml
import os
import re


def make_relative_path(source, path):
    relative_path = path[len(source):]
    if relative_path.startswith('/'):
        relative_path = relative_path[1:]
    # rel_dir = '.' if rel_dir is '' else rel_dir
    return relative_path


def get_id():
    return str(pymongo.collection.ObjectId())


def read_yaml(path):
    with open(path, 'r') as fp:
        data = yaml.load(fp)
    return data


def write_yaml(path, data):
    with open(path, 'w') as fp:
        yaml.dump(data, fp, default_flow_style=False)


def did_any_pattern_match(name, patterns):
    for pattern in patterns:
        if fnmatch.fnmatch(name, pattern):
            return True
    return False


def filter_list(lst, startswith=None, endswith=None, contains=None):
    filtered_list = []
    for s in lst:
        if startswith:
            if not s.startswith(startswith):
                break

        if endswith:
            if not s.endswith(endswith):
                break

        if contains:
            if contains not in s:
                break

        filtered_list.append(s)
    return filtered_list


def wildcard(pattern):
    result = glob.glob(pattern)
    if len(result) < 1:
        raise Exception
    return result if len(result) > 1 else result[0]


def split_label_file(path, label):
    base, ext = os.path.splitext(path)
    new_filename = "{}.{}{}".format(base, label, ext)
    return new_filename

def globre(path, pattern):
    return [os.path.join(path, f) for f in os.listdir(path) if re.search(pattern, f)]
