import logging as log
import pathlib
import re

import yaml

dicts = dict()

def setup_logging(level='INFO'):
    log.basicConfig(level=getattr(log, level), format='%(message)s')

def part_of(needle, haystack):
    return f' {needle}' in haystack or f',{needle}' in haystack

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
        if girls == 0 and boys == 0 and onegirl == 0 and others == 0:
            series = get_series_candidates(tags)
            if len(series) > 1:
                return False
        return not (girls > 0 or (boys + onegirl + others) > 1)

def get_series_candidates(tags):    # find series tags if they're included in other tags in parenthesis and also exist separately
    in_brackets = [re.sub(r'.+\((.+)\)$', r'\1', t) for t in tags if t.endswith(')') and '(' in t and '(object)' not in t]
    return [t for t in in_brackets if t in tags]

def tokenizer(tags): #coefficients found by Ridge regression
    naive = 4 # chosen by a fair dice roll...
    count = len(tags)
    length = len(','.join(tags))
    intercept = 3.7410189203217925
    return round(((0.75568025*count + 0.18637011 * length + intercept)*1.04 + length/naive)/2)