# Token Merging for Training (TMFT)

[![Python Application](https://github.com/yourusername/token-merging-4-training/actions/workflows/python-app.yml/badge.svg)](https://github.com/yourusername/token-merging-4-training/actions/workflows/python-app.yml)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Python tool designed to optimize and shorten Danbooru tags in image captions to save tokens during AI model training. This tool intelligently merges, filters, and consolidates tags while preserving semantic meaning, helping reduce token usage and improve training efficiency.

## Features

- **Smart Tag Merging** - Combines related tags (e.g., "short hair, black hair" → "short black hair")
- **Hierarchical Filtering** - Removes redundant tags when more specific versions exist
- **Blacklist Support** - Filters out unwanted or irrelevant tags
- **Animal-Specific Processing** - Handles animal character tags with specialized logic
- **Color Optimization** - Intelligently handles multicolored attributes
- **Batch Processing** - Process multiple text files at once
- **Token Estimation** - Reports approximate token savings
- **YAML Configuration** - Easily customizable rules and settings

## Prerequisites

- Python 3.10 or higher
- pip package manager

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/token-merging-4-training.git
   cd token-merging-4-training
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify installation:**
   ```bash
   python -m pytest tests/
   ```

## Usage

### Basic Usage

Process all text files in a directory:

```bash
python main.py "path/to/your/text/files"
```

### Example

Given an input file with tags:
```
long hair, black hair, red eyes, animal ears, cat ears, looking at viewer, multiple girls
```

The tool will output:
```
long black hair, red eyes, cat ears
```

**Token savings:** Approximately 8 tokens saved

### Processing Pipeline

The tool applies transformations in this order:

1. **Filtering** - Remove blacklisted tags and clip series information
2. **Hierarchy** - Remove redundant generic tags when specific ones exist
3. **Animal Processing** - Handle animal-specific tag logic
4. **Merging** - Combine tags with the same noun but different adjectives

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

### `config/synonyms.yaml`
```yaml
synonyms:
  footwear: boots
  eyewear: glasses
  headwear: hat
  # ... more synonyms
```

### `config/colors.yaml`
```yaml
- red
- blue
- green
- multicolored
# ... more colors
```

### `config/animals.yaml`
```yaml
- cat
- dog
- wolf
- tiger
# ... more animals
```

## API Documentation

### Core Functions

#### `process_tags(tags: list) -> list`
Main processing function that applies all transformations.

**Parameters:**
- `tags` (list): List of tag strings to process

**Returns:**
- `list`: Processed and optimized tags

**Example:**
```python
from pipeline import process_tags

input_tags = ["long hair", "black hair", "red eyes"]
result = process_tags(input_tags)
print(result)  # ['long black hair', 'red eyes']
```

#### Transform Modules

- **`transforms.filters`** - Tag filtering and blacklist operations
- **`transforms.hierarchy`** - Hierarchical tag processing and synonym replacement
- **`transforms.redundancy`** - Tag merging and redundancy removal

### Utility Functions

#### `utils.load_yaml_config(file: str) -> dict`
Load configuration from YAML files.

#### `utils.setup_logging(level: str = 'INFO')`
Configure logging for the application.

## Development

### Running Tests

```bash
python -m pytest tests/ -v
```

### Code Structure

```
token-merging-4-training/
├── config/                 # Configuration files
│   ├── animals.yaml
│   ├── blacklist.yaml
│   ├── colors.yaml
│   └── synonyms.yaml
├── transforms/             # Core transformation modules
│   ├── filters.py         # Filtering operations
│   ├── hierarchy.py       # Hierarchical processing
│   └── redundancy.py      # Merging and deduplication
├── tests/                 # Test files
├── main.py               # Main entry point
├── pipeline.py           # Processing pipeline
├── utils.py              # Utility functions
└── requirements.txt      # Dependencies
```

### Adding New Transformations

1. Create a new function in the appropriate `transforms/` module
2. Add the transformation to the pipeline in `pipeline.py`
3. Add corresponding tests in `tests/`
4. Update configuration files if needed

## Contributing

1. **Fork the repository**
2. **Create a feature branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes and add tests**
4. **Run the test suite:**
   ```bash
   python -m pytest tests/
   flake8 . --max-line-length=127
   ```
5. **Commit your changes:**
   ```bash
   git commit -am 'Add some feature'
   ```
6. **Push to the branch:**
   ```bash
   git push origin feature/your-feature-name
   ```
7. **Create a Pull Request**

### Code Style

- Follow PEP 8 guidelines
- Maximum line length: 127 characters
- Use meaningful variable and function names
- Add docstrings for all public functions
- Include type hints where appropriate

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact/Support

- **Issues:** [GitHub Issues](https://github.com/yourusername/token-merging-4-training/issues)
- **Discussions:** [GitHub Discussions](https://github.com/yourusername/token-merging-4-training/discussions)

For questions about usage or contributions, please open an issue on GitHub.

## Acknowledgments

- Inspired by the need to optimize token usage in AI model training
- Built for the Danbooru tagging community
- Thanks to all contributors who help improve this tool