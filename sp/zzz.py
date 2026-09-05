import os
import re
import unicodedata

base_folder = '.'
output_file = os.path.join(base_folder, 'zzzzzzzz.txt')
PREFIX = ''

processed_paths = []

def clean_filename(filename):
    name, ext = os.path.splitext(filename)
    name = unicodedata.normalize('NFKC', name).lower()

    # 1. Leading Junk Remove
    i = 0
    while i < len(name):
        cat = unicodedata.category(name[i])
        if cat.startswith('L') or cat.startswith('N'):
            break
        i += 1
    name = name[i:]

    # 2. Convert Middle Characters to Hyphen
    result = []
    for ch in name:
        cat = unicodedata.category(ch)
        if cat.startswith('L') or cat.startswith('N'):
            result.append(ch)
        else:
            result.append('-')

    name = ''.join(result)

    # 3. Cleanup Hyphens
    name = re.sub(r'-+', '-', name).strip('-')

    if not name:
        name = "file"

    if PREFIX and not name.startswith(PREFIX):
        name = PREFIX + name

    return f"{name}{ext}"


for root, dirs, files in os.walk(base_folder):
    for filename in files:
        if not filename.endswith('.html'):
            continue

        old_path = os.path.join(root, filename)
        new_name = clean_filename(filename)
        new_path = os.path.join(root, new_name)

        # Handle file name collision (যদি একই নামের অন্য ফাইল থাকে)
        if old_path != new_path and os.path.exists(new_path):
            name_part, ext_part = os.path.splitext(new_name)
            counter = 1
            while os.path.exists(os.path.join(root, f"{name_part}-{counter}{ext_part}")):
                counter += 1
            new_name = f"{name_part}-{counter}{ext_part}"
            new_path = os.path.join(root, new_name)

        # Execute Rename
        if old_path != new_path:
            try:
                os.rename(old_path, new_path)
                print(f"✅ Renamed: {filename} -> {new_name}")
            except Exception as e:
                print(f"❌ Failed to rename {filename}: {e}")
                continue
        else:
            print(f"ℹ️ Unchanged: {filename}")

        # Save relative path for ALL processed HTML files
        rel_folder = os.path.relpath(root, base_folder)
        if rel_folder == '.':
            rel_file_path = new_name
        else:
            rel_file_path = os.path.join(rel_folder, new_name).replace('\\', '/')

        processed_paths.append(rel_file_path)


# Save all HTML paths to text file
with open(output_file, 'w', encoding='utf-8') as f:
    for path in processed_paths:
        f.write(path + '\n')

print(f"\n✅ Total HTML files listed: {len(processed_paths)}")
print(f"✅ Path log saved to '{output_file}'")