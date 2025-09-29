# Token Merging for Training (TM4T)

[![Python Application](https://github.com/seedmanc/token-merging-4-training/actions/workflows/python-app.yml/badge.svg)](https://github.com/yourusername/token-merging-4-training/actions/workflows/python-app.yml)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/) 

A Python tool designed to optimize and shorten Danbooru tags in image captions to save tokens during AI model training. This tool intelligently merges, filters, and consolidates tags while preserving semantic meaning, helping reduce token usage and improve training efficiency.

## Features

- **Smart Tag Merging** - Combines related tags (e.g., "short hair, black hair" → "short black hair")
- **Hierarchical Filtering** - Removes redundant tags when more specific versions exist (breasts → large breasts)
- **Blacklist Support** - Filters out unwanted or irrelevant tags such as "commentary request"
- **Animal-Specific Processing** - Handles animal character tags with specialized logic (animal ears → dog ears)
- **Color Optimization** - Intelligently handles multicolored attributes (remove black,white,etc hair if multicolored hair)
- **Batch Processing** - Process multiple text files at once
- **Token Estimation** - Reports approximate token savings
- **YAML Configuration** - Easily customizable rules and settings

## Prerequisites

- pyyaml

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/seedmanc/token-merging-4-training.git
   cd token-merging-4-training
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ``` 

## Usage

### Basic Usage

Process all text files in a directory:

```bash
python main.py "path/to/your/txt/captions"
```
#### Also see the help:
```usage: main.py [-h] [--dry] [--author AUTHOR] [--class-tokens CLASS_TOKENS] [--brief | --verbose] [captions_path]

positional arguments:
  captions_path         Required.

optional arguments:
  -h, --help            show this help message and exit
  --dry                 Don't change the files
  --author AUTHOR       Replace author tag with --class-tokens + " style"
  --class-tokens CLASS_TOKENS
                        Replace --author tag with this. Defaults to --author w/o spaces or (...). Use --class-tokens= to remove author entirely.
  --brief               Reduce console spam
  --verbose
```
Edit YAML dictionaries as you see fit. The replace.yaml works as follows: the key will be replaced by one of the values under it but only if the values are found in the tags. So "adjusting eyewear, glasses" becomes "adjusting glasses, glasses" (with the duplicate removed further in processing).
Expand animals and colors dicts to ensure special processing of those categories (mainly to avoid "animal dog ears" entries, get rid of animal features if animal girl is already mentioned and remove colors if multicolored is present in the tags).
### Example console output:

```
python main.py C:\Users\USERNAME\Downloads\hukuro --author="poporu (hukuroneko)" --class-tokens=hukuro
FILE: __yak_kemono_friends_and_1_more_drawn_by_poporu_hukuroneko__da95e66e2af395a6c9c35f2eb732626f.txt
- commentary request
poporu (hukuroneko)  =>  hukuro style  b/c  --class-tokens
bow  =>  bowtie
brown bow  =>  brown bowtie
- ribbon  b/c  brown ribbon
- shirt  b/c  yellow shirt
- bowtie  b/c  brown bowtie
- horns  b/c  black horns
- breasts  b/c  large breasts
- animal ears  b/c  cow ears
- cow ears,cow horns  b/c  cow girl
- black horns,grey horns  b/c  multicolored
 - white hair
 - long hair
+ long white hair
- kemono friends 3,kemono friends  b/c  yak (kemono friends)
Saved ~43 tokens or 41%
['1girl', 'blush', 'brown bowtie', 'brown eyes', 'brown ribbon', 'cow girl', 'dress', 'extra ears', 'gloves', 'hair over one eye', 'highres', 'hukuro style', 'large breasts', 'long white hair', 'multicolored horns', 'short sleeves', 'smile', 'solo', 'twintails', 'yak (kemono friends)', 'yellow shirt']
```

### Processing Pipeline

The tool applies transformations in this order:

1. **Filtering** - Remove blacklisted tags and clip series information
2. **Hierarchy** - Remove redundant generic tags when specific ones exist
3. **Animal and color processing** - Handle specific tag logic
4. **Merging** - Combine tags with the same noun but different adjectives
5. **Artist conversion** - turn author tags into ready to use "style" class tokens for style-lora training or add if none present.

## Configuration

The tool uses YAML configuration files in the `config/` directory:

### `config/blacklist.yaml`
```yaml
- virtual youtuber
- looking at viewer
- multiple girls
- commentary request
# ... more blacklisted tags
```
These are removed unconditionally.

### `config/colors.yaml`
```yaml
- red
- blue
- green 
# ... more colors
```
Removes colored tags if multicolored/two-tone tag of the same subject is present.
### `config/animals.yaml`
```yaml
- cat
- dog
- wolf
- tiger
# ... more animals
```
Removes literal "animal part" if specific animal parts are present. Removes specific animal parts if that animal girl is present.

## Contact/Support

- **Issues:** [GitHub Issues](https://github.com/seedmanc/token-merging-4-training/issues) 

For questions about usage or contributions, please open an issue on GitHub.

## Acknowledgments

- Inspired by the need to optimize token usage in AI lora training
- Built for the *booru tagging community 