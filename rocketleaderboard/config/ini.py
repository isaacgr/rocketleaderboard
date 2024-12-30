from typing import Dict, Any, List, Tuple
import os
import configparser
import logging


log = logging.getLogger('config.ini')

# config.ini
CONFIG_SECTION = 'config'
HOSTS_SECTION = 'hosts'

RL_TRACKER_CONFIG_SECTION = 'config.rltracker'

RL_TRACKER_HOSTS_SECTION = 'hosts.rltracker'


def _maybe_transform_data_type(
    parser: configparser.ConfigParser,
    section: str,
    key: str
) -> int | float | bool | str:
    try:
        return parser.getboolean(section, key)
    except ValueError:
        pass
    try:
        return parser.getfloat(section, key)
    except ValueError:
        pass
    try:
        return parser.getint(section, key)
    except ValueError:
        pass
    return parser.get(section, key)


def _maybe_set_config_data_types(
    parser: configparser.ConfigParser
) -> Dict[str, Any]:
    data = dict()
    sections = parser.sections()
    for section in sections:
        items = parser.items(section)
        _items: List[Tuple[str, Any]] = []
        for item in items:
            key = item[0]
            value = _maybe_transform_data_type(parser, section, key)
            _items.append((key, value))
        data[section] = dict(_items)
    return data


def parse_ini_configuration(ini_path: str) -> Dict[str, Dict[str, Any]]:

    if not os.path.isfile(ini_path):
        raise Exception(
            'Unable to read config.ini. Was one created?',
            ini_path,
        )

    log.info('Reading config.ini.')
    parser = configparser.ConfigParser()
    parser.read_file(open(ini_path))

    data = _maybe_set_config_data_types(parser)
    return data


def parse_ini_authentication(ini_path: str) -> Dict[str, Dict[str, Any]]:

    if not os.path.isfile(ini_path):
        raise Exception('Unable to parse authentication.ini.')

    log.info('Reading authentication.ini.')
    parser = configparser.ConfigParser()
    parser.read_file(open(ini_path))

    data = _maybe_set_config_data_types(parser)
    return data
