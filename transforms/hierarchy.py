import logging as log
import re

from utils import dicts, part_of


def replace(tags):
    log.debug(':REPLACE')
    # brown footwear, boots => brown boots, boots
    joint = ','.join(tags)
    def replacer(tag):
        if len(tag.split(' ')) > 3: #skip long multiword tags, likely natural language
            return tag
        for key, values in dicts['replace'].items():
            if isinstance(values, str):     # singular values are for unconditional substitution
                if tag == key:
                    log.info(f"{tag}  =>  {values}")
                    return values
            else:                           # otherwise check if a substitute is also present in tags
                found = [v for v in values if part_of(key, joint) and part_of(v, joint)]
                if len(found) > 0:
                    tag2 = re.sub(r'(^|\s)('+re.escape(key)+r')(\s|$)', r'\1'+found[0]+r'\3', tag)
                    if tag2 != tag:
                        log.info(tag+'  =>  ' +tag2)
                        return tag2
        return tag
    return list(set([replacer(t) for t in tags]))

def _includes_or_plural(needle, haystack): # makes 'fishnets' be recognized as a part of 'fishnet pantyhose'
    # TODO: bug: makes 'shorts' to be considered a part of 'short hair'
    return haystack.endswith(' ' + needle) or haystack.startswith(needle + ' ') #or\
           #(haystack+'s').endswith(' ' + needle) or haystack.startswith(re.sub('s$','',needle)+' ')

def subsume(tags):
    log.debug(':SUBSUME')
    """Remove single-word tags that are suffixes or prefixes of other tags."""
    tags = list(set(tags))
    kept_tags = []
    for tag in tags:
        found = [t for t in tags if _includes_or_plural(tag, t) and not re.search(r'\d$', t)] #skip merging sequels
        if len(found) > 0:
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
