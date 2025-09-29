import glob
import logging as log
import re

import utils
from args import args
from pipeline import process_tags


def read_tags_from_file(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return sorted([tag.strip().lower().replace('_', ' ') for tag in re.split(r'\s*,\s*', f.read()) if tag != ''])


def write_tags_to_file(filename, tags):
    log.info(sorted(tags))
    if args.dry:
        return tags
    else:
        with open(filename, "w", encoding="utf-8") as f:
          f.write(', '.join(sorted(tags)))


if __name__ == "__main__":
    utils.setup_logging(args)
    for name in ['blacklist', 'replace', 'colors', 'animals']:
        utils.load_yaml_config(name)
    try:
        search_pattern = args.captions_path + "\\*.txt"
    except Exception:
        log.error('Missing captions path argument.')
        exit(1) #dumb pytest forces me to use this nonsense instead of making captions required
    original = 0
    saved_total = 0
    for file_path in glob.glob(search_pattern):
        log.warning("\nFILE: " + file_path.split('\\')[-1])
        input_tags = read_tags_from_file(file_path)
        tags = ', '.join(input_tags)
        log.debug('TAGS: '+tags)
        original_length = utils.tokenizer(input_tags)
        original += original_length
        log.debug(f'~{original_length} tokens in {len(input_tags)} tags and {len(tags)} characters')
        before = ','.join(input_tags)
        processed_tags = process_tags(input_tags)
        after = ','.join(processed_tags)
        saved = utils.tokenizer(input_tags) - utils.tokenizer(processed_tags)
        saved_total += saved
        log.warning(f"Saved ~{saved} tokens or {round(saved * 100 / original_length)}%")
        write_tags_to_file(file_path, processed_tags)
    log.warning(f'\nAVG savings: {round(saved_total * 100 / original)}%')
    if args.dry:
        log.warning('\nDry run, no files changed.')
