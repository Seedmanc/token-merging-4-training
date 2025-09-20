import logging as log
import re


def replace_synonym(tags, synonyms): #todo refactor
    log.debug(':REPLACE')
    # brown footwear, boots => brown boots, boots
    def replacer(tag):
        for key, value in synonyms.items():
            if (value in tags or (' '+value) in tags) and '(' not in tag:
                pattern = r'(^|\s)' + re.escape(key) + r'($|\s)'
                replacement = r'\1' + value + r'\2'
                tag2 = re.sub(pattern, replacement, tag)
                if tag2 != tag:
                    log.info(tag+'  =>  ' +tag2+'  b/c  '+[t for t in tags if value in t][0])
                    return tag2
        return tag
    return [replacer(t) for t in tags]


def subsume(tags):
    log.debug(':SUBSUME')
    """Remove single-word tags that are suffixes or prefixes of other tags."""
    tags = list(set(tags))
    kept_tags = []
    for tag in tags:
        found = [t for t in tags if (t.endswith(' ' + tag) or t.startswith(tag + ' '))]
        if len(found) > 0 and ' ' not in tag:
            log.info(f'- {tag}  b/c  {found[0]}')
        else:
            kept_tags.append(tag)
    return kept_tags


def specify_animal(tags, animals):
    log.debug(":SPECIFY")
    # Replace generic "animal" bodyparts with specific ones
    animal_parts = []
    for t in tags:
        if (len(t.split(' ')) == 2) and t.startswith('animal '):
            animal_parts.append(t)
    for ap in animal_parts:
        part = ap.split(' ')[1]
        if any([animal + ' ' + part in tags for animal in animals]):
            tags.remove('animal ' + part)
            log.info(
                '- animal ' + part + '  b/c  ' + ''.join([a for a in animals if a + ' ' + part in tags]) + ' ' + part)
    return tags
