from transforms.filters import remove_blacklisted
from transforms.redundancy import subsume, merge
from transforms.hierarchy import apply_synonym_replacement
from utils import load_yaml_config

def process_tags(tags):
    blacklist = load_yaml_config('blacklist.yaml')['blacklist']
    synonyms = load_yaml_config('synonyms.yaml')['synonyms']
    colors = load_yaml_config('colors.yaml')['colors']

    # Remove blacklisted tags
    tags = remove_blacklisted(tags, blacklist)
    # Synonym replacement
    tags = [apply_synonym_replacement(tag, tags, synonyms) for tag in tags]
    # Remove redundant tags
    tags = subsume(tags)
    # Merge tags
    tags = merge(tags, colors)
    return tags