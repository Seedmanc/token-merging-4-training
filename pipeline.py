from transforms.filters import remove_blacklisted, clip_after_series
from transforms.hierarchy import subsume, specify_animal
from transforms.redundancy import merge, omit_parts
from utils import load_yaml_config


def process_tags(tags):
    blacklist = load_yaml_config('blacklist.yaml')
    synonyms = load_yaml_config('synonyms.yaml')['synonyms']
    colors = load_yaml_config('colors.yaml')
    animals = load_yaml_config('animals.yaml')

    print('Pruning...')
    # Remove blacklisted tags and sequential groups of (...)
    tags = remove_blacklisted(tags, blacklist)
    tags = clip_after_series(tags)
    # Synonym replacement
    # tags = [apply_synonym_replacement(tag, tags, synonyms) for tag in tags]
    # Remove redundant tags "gloves, yellow gloves" => yellow gloves
    tags = subsume(tags)
    # Remove generic "animal *" body parts if specific animal part exists
    tags = specify_animal(tags, animals)
    # Remove specific animal parts if the girl is that animal
    tags = omit_parts(tags, animals)
    print('Merging...')
    # Merge tags "short hair, black hair" => "short black hair"
    tags = merge(tags, colors)
    return tags
