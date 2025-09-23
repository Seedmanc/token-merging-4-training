import logging as log
import re

from utils import dicts


def replace_synonym(tags): #todo refactor, unused
    log.debug(':REPLACE')
    # brown footwear, boots => brown boots, boots
    def replacer(tag):
        for key, value in dicts['synonyms'].items():
            if (value in tags or (' '+value) in tags) and '(' not in tag:
                pattern = r'(^|\s)' + re.escape(key) + r'($|\s)'
                replacement = r'\1' + value + r'\2'
                tag2 = re.sub(pattern, replacement, tag)
                if tag2 != tag:
                    log.info(tag+'  =>  ' +tag2+'  b/c  '+[t for t in tags if value in t][0])
                    return tag2
        return tag
    return [replacer(t) for t in tags]

def _includes_or_plural(needle, haystack): # makes 'fishnets' be recognized as a part of 'fishnet pantyhose'
    # TODO: bug: makes 'shorts' to be considered a part of 'short hair'
    return haystack.endswith(' ' + needle) or haystack.startswith(needle + ' ') or\
           (haystack+'s').endswith(' ' + needle) or haystack.startswith(re.sub('s$','',needle)+' ')

def subsume(tags):
    log.debug(':SUBSUME')
    """Remove single-word tags that are suffixes or prefixes of other tags."""
    tags = list(set(tags))
    kept_tags = []
    for tag in tags:
        found = [t for t in tags if _includes_or_plural(tag, t)]
        if len(found) > 0 and ' ' not in tag:
            log.info(f'- {tag}  b/c  {found[0]}')
        else:
            kept_tags.append(tag)
    return kept_tags

def specify_animal(tags):
    log.debug(":SPECIFY")
    # Drop generic "animal" bodyparts if specific exist
    animal_parts = []
    for t in tags:
        if (len(t.split(' ')) == 2) and t.startswith('animal '):
            animal_parts.append(t)
    for ap in animal_parts:
        part = ap.split(' ')[1]
        if any([animal + ' ' + part in tags for animal in dicts['animals']]):
            tags.remove('animal ' + part)
            log.info(
                '- animal ' + part + '  b/c  ' + ''.join([a for a in dicts['animals'] if a + ' ' + part in tags]) + ' ' + part)
    return tags
