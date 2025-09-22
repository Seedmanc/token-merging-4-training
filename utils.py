import logging as log
import pathlib
import re

import yaml

dicts = dict()

def setup_logging(level='INFO'):
    log.basicConfig(level=getattr(log, level), format='%(message)s')


def load_yaml_config(file):
    ROOT = pathlib.Path(__file__).resolve().parent
    with open(str(ROOT)+'/config/' + file + '.yaml') as stream:
        dicts[file] = yaml.safe_load(stream)

def is_solo(tags): #heuristic whether there's only one character, sum the girl(s) and boys
    if 'solo' in tags:
        return True
    else:
        girls = len([t for t in tags if re.match(r'\d\+?girls',t)])
        boys = len([t for t in tags if re.match(r'\d\+?boy(s)?',t)])
        others = len([t for t in tags if re.match(r'\d\+?other(s)?',t)])
        onegirl = len([t for t in tags if t == '1girl'])
        return not (girls > 0 or (boys + onegirl + others) > 1)