import re


def remove_blacklisted(tags, blacklist):
    return [tag for tag in tags if tag not in blacklist]


def clip_after_series(tags):  # remove after first group of () removing fan chars' authors like "name (series) (author)"
    return [re.sub(r'(\(.+\))\s.+', r'\1', tag) for tag in tags]
