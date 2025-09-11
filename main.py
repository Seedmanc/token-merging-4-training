import glob
from pipeline import process_tags

def read_tags_from_file(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return f.read().split(', ')

def write_tags_to_file(filename, tags):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(', '.join(sorted(tags)))

if __name__ == "__main__":
    search_pattern = "YOUR_INPUT_PATH/*.txt"
    for file_path in glob.glob(search_pattern):
        print(f"Processing file: {file_path}")
        input_tags = read_tags_from_file(file_path)
        before = ','.join(input_tags)
        processed_tags = process_tags(input_tags)
        after = ','.join(processed_tags)
        print(f"Saved ~{int((len(before)-len(after))/3.33)} tokens")
        write_tags_to_file(file_path, processed_tags)