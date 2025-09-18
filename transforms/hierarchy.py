import logging as log
import re


def apply_synonym_replacement(tag, all_tags, synonym_dict):
    for key, value in synonym_dict.items():
        if value in ','.join(all_tags) and '(' not in tag:
            pattern = r'(^|\s)' + re.escape(key) + r'($|\s)'
            replacement = r'\1' + value + r'\2'
            tag2 = re.sub(pattern, replacement, tag)
            if tag2 != tag:
                return tag2
    return tag


def subsume(tags):
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
