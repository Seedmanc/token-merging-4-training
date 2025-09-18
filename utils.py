import logging as log

import yaml


def setup_logging(level='INFO'):
    log.basicConfig(level=getattr(log, level), format='%(message)s')


def load_yaml_config(file):
    with open('config\\' + file) as stream:
        return yaml.safe_load(stream)
