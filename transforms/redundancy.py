import logging as log
from collections import defaultdict


def merge(tags, colors):
    """Merge several tags with the same noun into one tag with combined adjectives."""
    tags = list(set(tags))
    multi = {'multicolored', 'two-tone'}
    tree = defaultdict(list)

    for tag in tags:
        if '(' in tag:  # skip character names (usually have series in brackets)
            log.info(f'skip  {tag}  b/c (...)')
            continue
        words = tag.split(' ')
        if len(words) == 2:
            noun = words[-1]
            adj = words[0]
            for t in tags:
                if t != tag and t.endswith(noun) and len(t.split(' ')) == 2:
                    tree[noun].append(adj)

    for noun in tree.keys():
        if any([clr in multi for clr in tree[noun]]):
            removed_colors = [adj for adj in tree[noun] if adj in colors]
            tree[noun] = [adj for adj in tree[noun] if adj not in colors]
            log.info('- ' + ', '.join(removed_colors) + '  b/c multicolored')

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


def omit_parts(tags, animals):
    # Remove animal bodyparts if that animal is mentioned as a girl
    found_animals = [t for t in tags if t.endswith(" girl")]
    for kemono in found_animals:
        animal = kemono.split(' ')[0]
        if animal in animals:
            removed_tags = [t for t in tags if t.startswith(animal + ' ') and not t.endswith(' girl')]
            tags = [t for t in tags if not t.startswith(animal + ' ') or t.endswith(' girl')]
            log.info('- ' + (', '.join(removed_tags)) + '  b/c  ' + kemono)
    return tags
