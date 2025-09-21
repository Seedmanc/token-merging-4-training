from functools import reduce

from transforms.filters import remove_blacklisted, clip_after_series, remove_series
from transforms.hierarchy import subsume, specify_animal
from transforms.redundancy import merge, omit_parts, multicolor


def process_tags(tags):
    pipeline = [
        remove_blacklisted, clip_after_series, remove_series,
        #replace_synonym,
        subsume, specify_animal, omit_parts, multicolor,
        merge#, join
    ]
    return reduce(lambda t,f: f(t), pipeline, tags)
