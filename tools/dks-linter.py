import os
import yaml
import json
import jsonschema
import glob
import sys

# Configuration
SCHEMA_PATH = '../schemas/dks-header.schema.json'
DKS_EXTENSION = '.dks.md'

def load_schema():
    with open(SCHEMA_PATH, 'r') as f:
        return json.load(f)

def parse_dks_file(filepath):
    """
    Manually parses frontmatter to avoid external dependencies like python-frontmatter
    for this simple reference implementation.
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    if not content.startswith('---'):
        return None, "File must start with YAML frontmatter (---)"

    try:
        parts = content.split('---', 2)
        if len(parts) < 3:
            return None, "Frontmatter not closed properly"

        frontmatter = yaml.safe_load(parts[1])
        return frontmatter, None
    except yaml.YAMLError as e:
        return None, f"YAML Error: {e}"

def validate_project(root_dir):
    schema = load_schema()
    dks_files = glob.glob(os.path.join(root_dir, f"**/*{DKS_EXTENSION}"), recursive=True)

    print(f"🔍 Scanning {root_dir} for DKS files...")

    errors = 0
    seen_ids = set()

    for filepath in dks_files:
        print(f"  Checking {filepath}...", end=" ")
        meta, error = parse_dks_file(filepath)

        if error:
            print(f"❌\n    Error: {error}")
            errors += 1
            continue

        try:
            jsonschema.validate(instance=meta, schema=schema)

            # Semantic Checks
            if meta['id'] in seen_ids:
                print(f"❌\n    Error: Duplicate ID '{meta['id']}' found.")
                errors += 1
            else:
                seen_ids.add(meta['id'])
                print("✅")

        except jsonschema.ValidationError as e:
            print(f"❌\n    Schema Validation Error: {e.message}")
            errors += 1

    print("-" * 30)
    if errors == 0:
        print("🎉 All DKS files are valid!")
        sys.exit(0)
    else:
        print(f"found {errors} errors.")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python dks-linter.py <directory_to_scan>")
        sys.exit(1)

    validate_project(sys.argv[1])
