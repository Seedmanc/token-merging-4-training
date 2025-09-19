import logging as log
import re
from collections import defaultdict


def merge(tags):
    log.debug(':MERGE')
    """Merge several tags with the same noun into one tag with combined adjectives."""
    tags = list(set(tags))
    tree = defaultdict(list)

    for tag in tags:
        if '(' in tag:  # skip character names (usually have series in brackets)
            log.debug(f'skip  {tag}  b/c (...)')
            continue
        words = tag.split(' ')
        if len(words) == 2:
            noun = words[-1]
            adj = words[0]
            for t in tags:
                if t != tag and t.endswith(noun) and len(t.split(' ')) == 2:
                    tree[noun].append(adj)

    for noun in tree.keys():
        tree[noun] = list(set(tree[noun]))
        for adj in tree[noun]:
            try:
                tags.remove(adj + ' ' + noun)
                log.info(' - ' + adj + ' ' + noun)
            except Exception:
                pass
        merged = sorted(list(set(tree[noun])))
        log.info('+ ' + ' '.join(merged) + ' ' + noun)
        tags.append(' '.join(merged) + ' ' + noun)

    return tags


def multicolor(tags, colors):
    log.debug(':MULTI')
    """Remove colored objects if those are mentioned as multicolored."""
    multi = {'multicolored', 'two-tone'}

    for m in multi:
        parts = [re.sub(m+r'\s(.+)',r'\1',t) for t in tags if t.startswith(m+' ')]
        removed_tags = [t for t in tags if t.split(' ')[0] in colors and t.split(' ')[-1] in parts]
        if len(parts) > 0:
            log.info('- '+','.join(removed_tags)+'  b/c '+m)
        else:
            continue
        tags = [t for t in tags if t not in removed_tags]
    return tags


def omit_parts(tags, animals):
    log.debug(':OMIT')
    # Remove animal bodyparts if that animal is mentioned as a girl
    found_animals = [t for t in tags if t.endswith(" girl")]
    for kemono in found_animals:
        animal = kemono.split(' ')[0]
        if animal in animals:
            removed_tags = [t for t in tags if t.startswith(animal + ' ') and not t.endswith(' girl')]
            tags = [t for t in tags if not t.startswith(animal + ' ') or t.endswith(' girl')]
            log.info('- ' + (','.join(removed_tags)) + '  b/c  ' + kemono)
    return tags
