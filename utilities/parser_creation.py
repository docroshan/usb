import configparser
from collections import defaultdict


def create_config(section, key, value, file_name):
    config = configparser.ConfigParser()
    config.read(file_name)
    config.set(section, key, value)
    conf_file = open(file_name, 'w')
    config.write(conf_file)


def delete_key_value(section, keys, file_name):
    for i in keys:
        config = configparser.ConfigParser()
        config.read(file_name)
        config.remove_option(section, i)
        conf_file = open(file_name, 'w')
        config.write(conf_file)
        conf_file.close()


def read_config(file_name):
    d = defaultdict(str)
    config = configparser.ConfigParser()
    config.read(file_name)
    for i in config.sections():
        for key, value in config.items(i):
            d[key] += value

    return dict(d)


def get_attr(file_name, value):
    d = read_config(file_name)
    return d[value]
