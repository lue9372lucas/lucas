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

    # ---------- 1. REMOVE ONLY LEADING JUNK ----------
    i = 0
    while i < len(name):
        ch = name[i]
        cat = unicodedata.category(ch)

        # Stop at first letter or number (any language)
        if cat.startswith('L') or cat.startswith('N'):
            break

        i += 1

    name = name[i:]

    # ---------- 2. CONVERT MIDDLE ----------
    result = []

    for ch in name:
        cat = unicodedata.category(ch)

        # Keep all Unicode letters + numbers
        if cat.startswith('L') or cat.startswith('N'):
            result.append(ch)

        # Everything else becomes hyphen
        else:
            result.append('-')

    name = ''.join(result)

    # ---------- 3. CLEANUP ----------
    name = re.sub(r'-+', '-', name)   # collapse multiple hyphens
    name = name.strip('-')            # remove leading/trailing hyphens

    # Prevent empty filename
    if not name:
        name = "file"

    # Prevent double prefix
    if PREFIX and not name.startswith(PREFIX):
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