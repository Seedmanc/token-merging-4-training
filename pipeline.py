from transforms.filters import remove_blacklisted, clip_after_series, remove_series
from transforms.hierarchy import subsume, specify_animal, replace_synonym
from transforms.redundancy import merge, omit_parts, multicolor, join
from utils import load_yaml_config


def process_tags(tags):
    blacklist = load_yaml_config('blacklist.yaml')
    synonyms = load_yaml_config('synonyms.yaml')
    colors = load_yaml_config('colors.yaml')
    animals = load_yaml_config('animals.yaml')

    print('Pruning...')
    # Remove blacklisted tags and sequential groups of (...) as well as standalone series tag
    tags = remove_blacklisted(tags, blacklist)
    tags = clip_after_series(tags)
    tags = remove_series(tags)
    # Replace ambiguous overarching words by specific synonyms if they're already present (for merging later)
    tags = replace_synonym(tags, synonyms)
    # Remove redundant tags "gloves, yellow gloves" => yellow gloves
    tags = subsume(tags)
    # Remove generic "animal *" body parts if specific animal part exists
    tags = specify_animal(tags, animals)
    # Remove specific animal parts if the girl is that animal
    tags = omit_parts(tags, animals)
    # Remove colored parts if they're tagged as multicolored
    tags = multicolor(tags, colors)
    print('Merging...')
    # Merge tags "short hair, black hair" => "short black hair"
    tags = merge(tags)
    # Join tags that end and start with same word
    tags = join(tags)

    return tags
