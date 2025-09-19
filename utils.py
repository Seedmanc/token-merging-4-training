import logging as log
import pathlib

import yaml


def setup_logging(level='INFO'):
    log.basicConfig(level=getattr(log, level), format='%(message)s')


def load_yaml_config(file):
    ROOT = pathlib.Path(__file__).resolve().parent
    with open(str(ROOT)+'\\config\\' + file) as stream:
        return yaml.safe_load(stream)
