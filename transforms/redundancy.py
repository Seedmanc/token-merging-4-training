import logging as log
import re
from collections import defaultdict

from utils import dicts, is_solo


def merge(tags): #todo decide order: hair pink bow vs pink hair bow
    log.debug(':MERGE')
    """Merge several tags with the same noun into one tag with combined adjectives."""
    tags = list(set(tags))

    if not is_solo(tags):
        log.info('skip merging b/c multiple charas')
        return tags
    tree = defaultdict(list)

    for tag in tags:
        if '(' in tag:  # skip character names (usually have series in parenthesis)
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

def join(tags): #todo refactor,unused as of now
    log.debug(':JOIN')
    # white fur, fur trim => white fur trim
    heads ={t.split(' ')[0] for t in tags if re.match(r'^.+\s', t) and len(t.split(' ')) == 2}
    tails ={t.split(' ')[-1] for t in tags if re.search(r'\s.+$', t) and len(t.split(' ')) == 2}
    both = {h for h in heads if h in tails}
    for b in both:
        tails = list({t for t in tags if t.startswith(b+' ') and len(t.split(' ')) == 2})
        heads = list({t for t in tags if t.endswith(' '+b) and len(t.split(' ')) == 2})
        minlen = min(len(heads),len(tails))
        tails= tails[:minlen]
        heads= heads[:minlen]
        for h in heads:
            try:
                tags.remove(h)
                log.info(' - ' + h)
            except Exception:
                pass
            for t in tails:
                try:
                    tags.remove(t)
                    log.info(' - ' + t)
                except Exception:
                    pass
                add = (h+t).replace(b+b,b)
                tags.append(add)
                log.info('+ '+add)
    return tags

def multicolor(tags):
    log.debug(':MULTI')
    """Remove colored objects if those are mentioned as multicolored.""" #todo keep one color along with multicolored?
    multi = {'multicolored', 'two-tone'}

    for m in multi:
        parts = [re.sub(m+r'\s(.+)',r'\1',t) for t in tags if t.startswith(m+' ')]
        removed_tags = [t for t in tags if t.split(' ')[0] in dicts['colors'] and t.split(' ')[-1] in parts]
        if len(parts) > 0:
            log.info('- '+','.join(removed_tags)+'  b/c '+m)
        else:
            continue
        tags = [t for t in tags if t not in removed_tags]
    return tags


def omit_parts(tags):
    log.debug(':OMIT')
    # Remove animal bodyparts if that animal is mentioned as a girl
    found_animals = [t for t in tags if t.endswith(" girl")]
    for kemono in found_animals:
        animal = kemono.split(' ')[0]
        if animal in dicts['animals']:
            removed_tags = [t for t in tags if t.startswith(animal + ' ') and not t.endswith(' girl')]
            tags = [t for t in tags if not t.startswith(animal + ' ') or t.endswith(' girl')]
            log.info('- ' + (','.join(removed_tags)) + '  b/c  ' + kemono)
    return tags

def andjoin(tags):
    log.debug(':ANDJOIN')
    # yellow hair, yellow boots => yellow hair and boots #todo check if the confusion is worth the tokens
    tree = defaultdict(list)
    for t in tags:
        pair = t.split(' ')
        if len(pair) == 2:
            tree[pair[0]].append(pair[1])

    for adj,nouns in tree.items():
        if (len(nouns) == 2):
            try:
                toremove = ' '.join(nouns)
                tags.remove(adj+' '+nouns[0])
                tags.remove(adj+' '+nouns[1])
                log.info(' - '+adj+' '+nouns[0]+','+adj+' '+nouns[1])
                toadd =' '.join([adj,' and '.join(sorted(nouns))])
                tags.append(toadd)
                log.info('+ '+ toadd)
            except Exception:
                pass
    return tags