import sys
import re

def green(text):
    return f"\033[92m{text}\033[0m"

def red(text):
    return f"\033[91m{text}\033[0m"

def yellow(text):
    return f"\033[93m{text}\033[0m"

def bold(text):
    return f"\033[1m{text}\033[0m"

def strip_ansi_codes(text):
    # Regex pattern to match ANSI escape codes
    ansi_escape_pattern = r"\x1B[@-_][0-?]*[ -/]*[@-~]"
    return re.sub(ansi_escape_pattern, "", text)

def parse_line(line):
    if not line.startswith("tests/"):
        return None

    # Split the line into parts using "::" as the delimiter
    line = line.strip()
    line = re.sub('\s{2,}', ' ', line)
    line = re.sub(' ', '::', line, count=1)
    parts = line.strip().split("::")
    if len(parts) < 2:
        return None

    # Extract the file path, describe blocks, test name, status, and progress
    file_path = bold(parts[0].replace("tests/", ""))
    describe_blocks = parts[1:-2]  # All describe blocks
    test_name = parts[-2]#.replace("_", " ")
    status = parts[-1]
    status = strip_ansi_codes(status)
    status = re.sub('\[\s*\d+%\]$', '', status).strip()

    if status == "PASSED":
        test_name = green(test_name)
        status = green("✔")
    elif status == "FAILED":
        test_name = red(test_name)
        status = red("✘")
    elif status == "SKIPPED":
        test_name = yellow(test_name)
        status = yellow("⚠")

    # Construct the hierarchical dictionary
    hierarchy = {}
    current_level = hierarchy
    for block in describe_blocks:
        block = block#.replace("_", " ")
        current_level[block] = {}
        current_level = current_level[block]

    # Add the test name and status
    current_level[test_name] = f"{status}"
    return {file_path: hierarchy}

def merge_dicts(existing, new):
    """
    Merge two hierarchical dictionaries recursively.
    """
    for key, value in new.items():
        if key in existing:
            if isinstance(value, dict) and isinstance(existing[key], dict):
                # Recursively merge nested dictionaries
                merge_dicts(existing[key], value)
            else:
                # Overwrite non-dictionary values (e.g., test statuses)
                existing[key] = value
        else:
            # Add new keys to the dictionary
            existing[key] = value

def format_output(hierarchy, indent=0):
    """
    Recursively format and print the hierarchical dictionary.
    """
    for key, value in hierarchy.items():
        # Filter out "describe_" and "it_" prefixes, and replace underscores with spaces
        filtered_key = key.replace("describe_", "") \
                          .replace("it_", "") \
                          .replace("_", " ")

        print()
        if isinstance(value, dict):
            print(f"{'  ' * indent}- {filtered_key}", end='')
            format_output(value, indent + 1)
        else:
            print(f"{'  ' * indent}  {value} {filtered_key}", end='')


def main():
    # Initialize an empty dictionary to store the hierarchical structure
    test_hierarchy = {}

    # Read each line from stdin
    for line in sys.stdin:
        parsed = parse_line(line)
        if parsed:
            merge_dicts(test_hierarchy, parsed)
        else:
            print(line, end='')

    # Print the formatted output
    format_output(test_hierarchy)
    print()

if __name__ == "__main__":
    main()
