import logging as log
import re


def remove_blacklisted(tags, blacklist):
    return [tag for tag in tags if tag not in blacklist]


def clip_after_series(tags):  # remove after first group of () removing fan chars' authors like "name (series) (author)"
    return [re.sub(r'(\(.+\))\s.+', r'\1', tag) for tag in tags]


def remove_series(tags):
    log.debug(':SERIES')
    series_candidates = [re.sub(r'.+\((.+)\)$', r'\1', t) for t in tags if t.endswith(')')]
    for s in series_candidates:
        removed_tags = [t for t in tags if t == s]
        log.info('- '+','.join(removed_tags)+'  b/c  '+[t for t in tags if t.endswith(s+')')][0])
        tags = list(filter(lambda t: t not in removed_tags, tags))
    return tags