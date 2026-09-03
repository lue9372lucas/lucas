import os
import re
import unicodedata

# Base folder
base_folder = '.'

# Output file
output_file = os.path.join(base_folder, 'zzzzzzzz.txt')

# Prefix
PREFIX = ''

# Store renamed files
new_names = []


# Filename cleaner
def clean_filename(filename):
    name, ext = os.path.splitext(filename)

    # Normalize unicode characters
    name = unicodedata.normalize('NFKC', name)

    # Convert to lowercase
    name = name.lower()

    # Remove special symbols
    # Keep:
    # - unicode letters
    # - numbers
    # - spaces
    # - hyphens
    # - underscores
    name = re.sub(r'[^\w\s-]', ' ', name, flags=re.UNICODE)

    # Replace spaces/underscores with hyphen
    name = re.sub(r'[-\s]+', '-', name, flags=re.UNICODE)

    # Remove extra hyphens
    name = name.strip('-')

    # Prevent double prefix
    if not name.startswith(PREFIX):
        name = PREFIX + name

    return f"{name}{ext}"


# Walk through all folders
for root, dirs, files in os.walk(base_folder):

    for filename in files:

        # Process only HTML files
        if not filename.endswith('.html'):
            continue

        old_path = os.path.join(root, filename)

        # Generate new filename
        new_name = clean_filename(filename)

        # Skip if unchanged
        if new_name == filename:
            continue

        new_path = os.path.join(root, new_name)

        try:
            # Rename file
            os.rename(old_path, new_path)

            # Relative path
            rel_folder = os.path.relpath(root, base_folder)

            rel_file_path = os.path.join(
                rel_folder,
                new_name
            ).replace('\\', '/')

            new_names.append(rel_file_path)

            print(f"✅ Renamed: {filename} -> {new_name}")

        except Exception as e:
            print(f"❌ Failed to rename {filename}: {e}")


# Save renamed filenames
with open(output_file, 'w', encoding='utf-8') as f:
    for name in new_names:
        f.write(name + '\n')

print(f"\n✅ Renamed {len(new_names)} HTML files")
print(f"✅ Saved list to '{output_file}'")