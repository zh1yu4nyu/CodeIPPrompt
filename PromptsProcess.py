# Usage: python3 PromptsProcess.py <prompt_dir>
# Example: python3 PromptsProcess.py prompts_agpl3_python_2023-03-27-21-21-29

import os
import sys
import time

prompt_dir = sys.argv[1]

check_prompt_dir = os.path.join("Prompts", prompt_dir)
check_source_dir = os.path.join("Source", prompt_dir.replace("prompts", "source"))
check_meta_path = os.path.join(check_source_dir, "meta_" + prompt_dir.split("_")[-1] + ".csv")

# Get the list of file names in the prompt directory
prompt_files = os.listdir(check_prompt_dir)
source_files = os.listdir(check_source_dir)

# Check content of prompts
for file in prompt_files:
    prompt_path = os.path.join(check_prompt_dir, file)

    # If file path contains special character, remove it
    if any(c in '`|<>()"*?: ' for c in prompt_path) or any(ord(c) > 127 for c in prompt_path) or any(u'\u4e00' <= c <= u'\u9fff' for c in prompt_path):
        print("File: " + file + " contains special character. Deleting.")
        os.remove(prompt_path)
        continue

    if os.stat(prompt_path).st_size == 0:
        print("File: " + file + " is empty. Deleting.")
        os.remove(prompt_path)


# Open the meta file
with open(check_meta_path, 'r') as meta_file:
    lines = meta_file.readlines()

# Initialize an empty list to store the updated lines
updated_lines = []
meta_filenames = []

# Loop through the lines in the meta file
for line in lines:
    # Get the file name from the second column, if "/" exists then extract the last item splitted by "/"
    if "/" in line.split(",")[1]:
        filename = line.split(",")[1].split("/")[-1]
    else:
        filename = line.split(",")[1]
    meta_filenames.append(filename)
    
    if os.path.exists(os.path.join(check_prompt_dir, filename)) and os.path.exists(os.path.join(check_source_dir, filename)):
        updated_lines.append(line)
    else:
        print(f"{filename} exists in meta but does not exist in the prompt or source directory, deleting...")
        if os.path.exists(os.path.join(check_prompt_dir, filename)):
            os.remove(os.path.join(check_prompt_dir, filename))
        if os.path.exists(os.path.join(check_source_dir, filename)):
            os.remove(os.path.join(check_source_dir, filename))

# Write the updated lines back to the meta file
with open(check_meta_path, 'w') as meta_file:
        
    meta_file.writelines(updated_lines)
    print(f"Done writing {len(updated_lines)} lines to meta file...")

# Loop through the files in the source directory
for filename in source_files:
    # If the file is a csv file, skip it
    if filename.endswith(".csv"):
        continue
    # Check if the file exists in the prompt directory and updated_lines
    if filename in prompt_files and filename in meta_filenames:
        continue
    else:
        print(f"{filename} exists in source but does not exist in the prompt or meta file, deleting...")
        os.remove(os.path.join(check_source_dir, filename))
        if os.path.exists(os.path.join(check_prompt_dir, filename)):
            os.remove(os.path.join(check_prompt_dir, filename))    
        
for filename in prompt_files:
    # Check if the file exists in the source directory and updated_lines
    if filename in source_files and filename in meta_filenames:
        continue
    else:
        print(f"{filename} exists in prompt but does not exist in the source or meta file, deleting...")
        os.remove(os.path.join(check_prompt_dir, filename))
        if os.path.exists(os.path.join(check_source_dir, filename)):
            os.remove(os.path.join(check_source_dir, filename))
