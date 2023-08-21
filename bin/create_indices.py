import os
import re
import json

# Regex sorcery, don't ask me how it works, I don't know either
proc_pattern = re.compile(r'(/[\w/]+)?\s*proc/(\w+)\((.*?)\)')
comment_pattern = re.compile(r'\/\/(.*)')

# What to index aka where DM files are located
DIRECTORY = '../code'

# Directory to save the output JSON files
OUTPUT_DIRECTORY = '../index'

# Create the output directory if it doesn't exist
if not os.path.exists(OUTPUT_DIRECTORY):
    os.makedirs(OUTPUT_DIRECTORY)

# Extracting unique top-level directories within DIRECTORY
top_level_folders = [d for d in os.listdir(DIRECTORY) if os.path.isdir(os.path.join(DIRECTORY, d))]

for folder in top_level_folders:
    index = []
    
    # Looping through each file in the top-level directory and its subdirectories
    for root, _, files in os.walk(os.path.join(DIRECTORY, folder)):
        for file in files:
            if file.endswith('.dm'):
                with open(os.path.join(root, file), 'r', encoding='utf-8', errors='ignore') as f:
                    lines = f.readlines()
                    for i, line in enumerate(lines):
                        # Check for procs
                        match = proc_pattern.search(line)
                        if match:
                            proc = {
                                'proc_name': match.group(2),
                                'full_path': match.group(0),
                                'file_location': os.path.join(root, file),
                                'line_number': i + 1,
                                'arguments': [arg.strip() for arg in match.group(3).split(",") if arg.strip()],
                                'comment': None
                            }

                            # Check for comments on the preceding line - completely useless, but I'm keeping it for my own shenanigan purposes
                            comment_match = comment_pattern.search(lines[i - 1])
                            if comment_match:
                                proc['comment'] = comment_match.group(1).strip()

                            index.append(proc)

    # Save the index for the specific folder to a JSON file in the output directory
    output_path = os.path.join(OUTPUT_DIRECTORY, folder + "_index.json")
    with open(output_path, 'w') as outfile:
        json.dump(index, outfile, indent=4)

    print(f"Indexing for top-level folder {folder} completed.")
