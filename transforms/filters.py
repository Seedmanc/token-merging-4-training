import logging as log
import re

from utils import dicts


def remove_blacklisted(tags): #remove blacklisted tags supporting wildcards *
    tags = [tag for tag in tags if tag not in dicts['blacklist']]
    for b in dicts['blacklist']:
        if b.startswith('*'):
            tags = [t for t in tags if not t.endswith(b[1:])]
        elif b.endswith('*'):
            tags = [t for t in tags if not t.startswith(b[:-1])]
    return tags


def clip_after_series(tags):  # remove after first group of () removing fan chars' authors like "name (series) (author)"
    return [re.sub(r'(\(.+\))\s.+', r'\1', tag) for tag in tags]


def remove_series(tags): #remove separate tag with series if those are included in character tags
    log.debug(':SERIES')
    series_candidates = [re.sub(r'.+\((.+)\)$', r'\1', t) for t in tags if t.endswith(')') and '(' in t]
    for s in series_candidates:
        removed_tags = [t for t in tags if t == s or re.match(re.escape(s)+'\\s\\d', t)]
        if len(removed_tags) > 0:
            log.info('- '+','.join(removed_tags)+'  b/c  '+[t for t in tags if t.endswith(s+')')][0])
            tags = list(filter(lambda t: t not in removed_tags, tags))
    return tags

def alternate_costume(tags): #remove "official" from "alternate costume" since SD doesn't seem to profit from it
    return [t.replace('official alternate costume', 'alternate costume') for t in tags]

#todo - fishnet(s)