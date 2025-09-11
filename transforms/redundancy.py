def subsume(tags):
    """Remove tags that are suffixes or prefixes of other tags."""
    tags = list(set(tags))
    kept_tags = []
    for tag in tags:
        found = any([(t.endswith(tag) or t.startswith(tag)) and t != tag for t in tags])
        if not found and tag != '':
            kept_tags.append(tag)
    return kept_tags

def merge(tags, colors):
    """Merge two-word tags with the same noun into one tag with combined adjectives."""
    from collections import defaultdict
    tags = list(set(tags))
    tree = defaultdict(list)
    for tag in tags:
        if '(' in tag:
            continue
        words = tag.split(' ')
        if len(words) == 2:
            noun = words[-1]
            adj = words[0]
            for t in tags:
                if t != tag and t.endswith(noun) and len(t.split(' ')) == 2:
                    tree[noun].append(adj)
    for noun, adjs in tree.items():
        if 'multicolored' in adjs and noun == 'hair':
            adjs = [adj for adj in adjs if adj not in colors]
        for adj in adjs:
            tag_to_remove = f"{adj} {noun}"
            if tag_to_remove in tags:
                tags.remove(tag_to_remove)
        merged = list(set(adjs))
        tags.append(' '.join(merged) + ' ' + noun)
    return tags