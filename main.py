import glob
import logging as log
import re
import sys

import utils
from pipeline import process_tags


def read_tags_from_file(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return sorted([tag.strip().lower().replace('_', ' ') for tag in re.split(r'\s*,\s*', f.read()) if tag != ''])


def write_tags_to_file(filename, tags):
    log.info(sorted(tags))
    return tags
    # with open(filename, "w", encoding="utf-8") as f:
    # f.write(', '.join(sorted(tags)))


if __name__ == "__main__":
    utils.setup_logging('DEBUG')
    search_pattern = sys.argv[1] + "\\*.txt"
    for file_path in glob.glob(search_pattern):
        log.info("FILE: " + file_path.split('\\')[-1])
        input_tags = read_tags_from_file(file_path)
        log.info(input_tags)
        before = ','.join(input_tags)
        processed_tags = process_tags(input_tags)
        after = ','.join(processed_tags)
        log.info(f"Saved ~{int((len(before) - len(after)) / 3.33)} tokens")
        write_tags_to_file(file_path, processed_tags)
