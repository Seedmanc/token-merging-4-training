import logging as log
import re

from utils import dicts, get_series_candidates


def remove_blacklisted(tags): #remove blacklisted tags supporting wildcards *
    log.debug(':BLACKLIST')
    removed = [tag for tag in tags if tag in dicts['blacklist']]
    for b in dicts['blacklist']:
        if b.startswith('*'):
            removed += [t for t in tags if t.endswith(b[1:])]
        elif b.endswith('*'):
            removed += [t for t in tags if t.startswith(b[:-1])]
    if (len(removed) > 0):
        log.info('- '+','.join(removed)+'  b/c blacklist')
        tags = [t for t in tags if t not in removed]
    return tags


def clip_after_series(tags):  # remove after first group of () removing fan chars' authors like "name (series) (author)"
    return [re.sub(r'(\(.+\))\s.+', r'\1', tag) for tag in tags]


def remove_series(tags): #remove separate tag with series if those are included in character tags
    log.debug(':SERIES')
    series_candidates = get_series_candidates(tags)
    for s in series_candidates:
        removed_tags = [t for t in tags if t == s or re.match(re.escape(s)+'\\s\\d', t)]
        if len(removed_tags) > 0:
            log.info('- '+','.join(removed_tags)+'  b/c  '+[t for t in tags if t.endswith(s+')')][0])
            tags = list(filter(lambda t: t not in removed_tags, tags))
    return tags

def alternate_costume(tags): #remove "official" from "alternate costume" since SD doesn't seem to profit from it
    return [t.replace('official alternate costume', 'alternate costume') for t in tags]

#todo - fishnet(s)