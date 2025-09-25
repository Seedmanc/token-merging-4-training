from functools import reduce

from transforms.filters import remove_blacklisted, clip_after_series, remove_series, alternate_costume
from transforms.hierarchy import subsume, specify_animal
from transforms.redundancy import merge, omit_parts, multicolor, andjoin


def process_tags(tags):
    pipeline = [
        remove_blacklisted, clip_after_series, alternate_costume,
        #replace_synonym,
        subsume, specify_animal, omit_parts, multicolor,
        merge, remove_series, andjoin#, join
    ]
    return reduce(lambda t,f: f(t), pipeline, tags)
