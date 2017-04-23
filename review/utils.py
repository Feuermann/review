import os
from configparser import ConfigParser


def read_config_section(config_path, section):
    """Read section from config file.
    Read section with specified name from config file at specified path.

    """

    if not os.path.exists(config_path):
        raise ValueError('Could not find config file at path %s'.format(config_path))

    if not os.path.exists(config_path):
        raise ValueError('Could not find config file at path %s' % config_path)

    try:
        config = ConfigParser()
        config.read(config_path, encoding="utf8")

    except Exception as e:
        raise ValueError('Problem with read config: %s' % (str(e)))

    if section not in config:
        raise ValueError("Could not find section %s in config file" % (section))

    config_section = dict(config[section])

    return config_section
