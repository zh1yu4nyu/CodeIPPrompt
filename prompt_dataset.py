# Usage: python3 prompt_dataset.py <dataset_name> <source_dir> <prompt_num>
# Example: python3 prompt_dataset.py codeparrot your_path_to_source 10000

import re
import os
import sys
import csv
import json
import random
import datetime
import pyarrow.parquet as pq


dataset_name = sys.argv[1]
dataset_dir = sys.argv[2]
prompt_num = sys.argv[3]

def source_codeparrot(prompt_num):

    now_time = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

    # Make a directory to store the source files and metadata
    source_dir = "Source/source_" + "codeparrot" + "_" + str(prompt_num) + "_" + now_time
    os.mkdir(source_dir)
    meta_csv = os.path.join(source_dir, "meta" + "_" + now_time + ".csv")

    # Write header to the csv file, ["repo_name", "path", "license", "language"]
    with open(meta_csv, "w") as f:
        writer = csv.writer(f)
        writer.writerow(["repo_name", "path", "license", "language"])

    # Path to the codeparrot dataset that contains all the json files
    file_list = os.listdir(dataset_dir)
    file_list = [os.path.join(dataset_dir, file) for file in file_list if file.endswith(".json")]

    random.shuffle(file_list)

    now_prompt_num = 0
    
    while now_prompt_num < int(prompt_num):
        for file_path in file_list:

            with open(file_path, "r") as f:
                lines = f.readlines()

                # Use the randint function to generate random line numbers
                line_numbers = [random.randint(0, len(lines)-1) for _ in range(int(prompt_num))]

                for line_number in line_numbers:
                    if not now_prompt_num < int(prompt_num):
                        return source_dir, meta_csv
                    else:
                        line = lines[line_number]
                        data = json.loads(line)
                        repo_name = data["repo_name"]
                        path = data["path"]
                        code = data["content"]
                        license = data["license"]

                        # If license is  "unlicense", "", or does not include Creative Commons
                        if license in ["unlicense", ""] and "cc" not in license:
                            continue

                        # Get the file name and the file extension, which is in the last part of path
                        file_name = path.split("/")[-1]

                        if os.path.exists(os.path.join(source_dir, file_name)):
                            # Count the number of files with the same name
                            file_num = 0
                            for file in os.listdir(source_dir):
                                if file.startswith(file_name.split(".")[0]):
                                    file_num += 1

                            # Add the number to the end of the file name
                            file_name = file_name.split(".")[0] + "_" + str(file_num) + "." + file_extension

                        # All the files in the codeparrot dataset are Python files
                        language = "Python"

                        # Write the metadata to the file
                        with open(meta_csv, "a") as f:
                            writer = csv.writer(f)
                            writer.writerow([repo_name, file_name, license, language])
                            f.close()

                        now_prompt_num += 1
                    
    return source_dir, meta_csv


def source_thepile(prompt_num):
    
        now_time = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    
        # Make a directory to store the source files and metadata
        source_dir = "Source/source_" + "thepile" + "_" + str(prompt_num) + "_" + now_time
        os.mkdir(source_dir)
        meta_csv = os.path.join(source_dir, "meta" + "_" + now_time + ".csv")
    
        # Write header to the csv file, ["repo_name", "path", "license", "language"]
        with open(meta_csv, "w") as f:
            writer = csv.writer(f)
            writer.writerow(["repo_name", "path", "license", "language"])
    
        file_list = os.listdir(dataset_dir)
        file_list = [os.path.join(dataset_dir, file) for file in file_list if file.endswith(".jsonl")]
        # Randomize the order of the file list
        random.shuffle(file_list)

        now_prompt_num = 0
        
        while now_prompt_num < int(prompt_num):
            for file_path in file_list:

                with open(file_path, "r") as f:
                    lines = f.readlines()
                    random.shuffle(lines)

                    for line in lines:
                        if not now_prompt_num < int(prompt_num):
                            return source_dir, meta_csv
                        else:
                            data = json.loads(line)
                            repo_name = data['meta']["repo_name"]
                            file_name = data['meta']['file_name']
                            code = data["text"]

                            # Set license to "unknown" for now to make format consistent, we can sort the license with postprocessing
                            license = "unknown"

                            # Get the file extension
                            file_extension = file_name.split(".")[-1]

                            if file_extension not in ["c", "cc", "cpp", "java", "cs", "py"]:
                                continue
                            else:
                                # Check if the file already exists
                                if os.path.exists(os.path.join(source_dir, file_name)):
                                    # Count the number of files with the same name
                                    file_num = 0
                                    for file in os.listdir(source_dir):
                                        if file.startswith(file_name.split(".")[0]):
                                            file_num += 1

                                    # Add the number to the end of the file name
                                    file_name = file_name.split(".")[0] + "_" + str(file_num) + "." + file_extension
                                
                                # Write the source code to the file
                                with open(os.path.join(source_dir, file_name), "w") as f:
                                    f.write(code)
                                    f.close()
                    
                                # The file extension of thepile is not consistent, so it needs to be converted
                                if file_extension == "c":
                                    language = "C"
                                elif file_extension == "cc" or file_extension == "cpp":
                                    language = "C++"
                                elif file_extension == "java":
                                    language = "Java"
                                elif file_extension == "cs":
                                    language = "C#" 
                                elif file_extension == "py":
                                    language = "Python"

                                # Write the metadata to the file
                                with open(meta_csv, "a") as f:
                                    writer = csv.writer(f)
                                    writer.writerow([repo_name, file_name, license, language])
                                    f.close()

                                now_prompt_num += 1

        return source_dir, meta_csv

def source_gcpy(prompt_num):
    
        now_time = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    
        # Make a directory to store the source files and metadata
        source_dir = "Source/source_" + "gcpy" + "_" + str(prompt_num) + "_" + now_time
        os.mkdir(source_dir)
        meta_csv = os.path.join(source_dir, "meta" + "_" + now_time + ".csv")
    
        # Write header to the csv file, ["repo_name", "path", "license", "language"]
        with open(meta_csv, "w") as f:
            writer = csv.writer(f)
            writer.writerow(["repo_name", "path", "license", "language"])
    
        file_list = os.listdir(dataset_dir)
        # Find the file list that does not have any extension in the folder
        file_list = [os.path.join(dataset_dir, file) for file in file_list if "." not in file]

        # Randomize the order of the file list
        random.shuffle(file_list)

        now_prompt_num = 0
        
        while now_prompt_num < int(prompt_num):
            for file_path in file_list:

                df = pq.read_table(source=file_path).to_pandas()
                df_shuffled = df.sample(frac=0.5, replace=False)
                
                for index, row in df_shuffled.iterrows():
                    if index == 0:
                        continue
                    if not now_prompt_num < int(prompt_num):
                        return source_dir, meta_csv
                    else:
                        code = row["content"]
                        license = row["license"]
                        repo_name = row["repo_name"]
                        path = row["path"]

                        # If license is  "unlicense", "", or does not include Creative Commons
                        if license in ["unlicense", ""] and "cc" not in license:
                            continue                        
                        
                        # Get the file name
                        if "/" in path:
                            file_name = path.split("/")[-1]
                        else:
                            file_name = path

                        # Get the file extension
                        file_extension = file_name.split(".")[-1]

                        if file_extension not in ["c", "cpp", "java", "cs", "py"]:
                            continue
                        else:
                            # Check if the file already exists
                            if os.path.exists(os.path.join(source_dir, file_name)):
                                # Count the number of files with the same name
                                file_num = 0
                                for file in os.listdir(source_dir):
                                    if file.startswith(file_name.split(".")[0]):
                                        file_num += 1

                                # Add the number to the end of the file name
                                file_name = file_name.split(".")[0] + "_" + str(file_num) + "." + file_extension
                            
                            # Write the source code to the file
                            with open(os.path.join(source_dir, file_name), "w") as f:
                                f.write(code)
                                f.close()
                
                            # The file extension of thepile is not consistent, so it needs to be converted
                            if file_extension == "c":
                                language = "C"
                            elif file_extension == "cc" or file_extension == "cpp":
                                language = "C++"
                            elif file_extension == "java":
                                language = "Java"
                            elif file_extension == "cs":
                                language = "C#" 
                            elif file_extension == "py":
                                language = "Python"

                            # Write the metadata to the file
                            with open(meta_csv, "a") as f:
                                writer = csv.writer(f)
                                writer.writerow([repo_name, file_name, license, language])
                                f.close()

                            now_prompt_num += 1

        return source_dir, meta_csv


# Generate prompts based on the source files, whose paths are stored in the file "source_paths.csv"
def prompt_dataset(source_dir):

    python_pattern1 = re.compile(r'^\s*#.*')
    python_pattern2 = re.compile(r'""".*?"""')
    python_pattern3 = re.compile(r"'''.*?'''")
    ccsjava_pattern1 = re.compile(r'^\s*//.*')
    ccsjava_pattern2 = re.compile(r'/\*.*?\*/')

    pattern_func = re.compile(r'^\s*def\s+\w+')
    pattern_cfunc = re.compile(r'^(?!.*\b(if|else|while|for|switch|case|struct|typedef|return)\b)(?<!;)\s*\w+\s+\w+\s*\([^=;]+\)(?<!\s;)\s*$')
    pattern_class = re.compile(r'^\s*class\s+\w+')
    pattern_public = re.compile(r'^\s*public\s+\w+')
    pattern_private = re.compile(r'^\s*private\s+\w+')
    pattern_protected = re.compile(r'^\s*protected\s+\w+')

    # Make a directory to store the prompts and metadata
    prompt_dir = "Prompts/prompts_" + source_dir.split("_", 1)[1]
    os.mkdir(prompt_dir)

    # Loop through all the programs in the source directory
    for f in os.listdir(source_dir):
        if (f.endswith(".py") or f.endswith(".c") or f.endswith(".cpp") or f.endswith(".java") or f.endswith(".cs")) and not any(u'\u4e00' <= c <= u'\u9fff' for c in f):
            file_path = os.path.join(source_dir, f)
            prompt_path = os.path.join(prompt_dir, f)

            with open(file_path, "r") as infile, open(prompt_path, "w") as outfile:
                # Loop through the line number of infile
                for i, line in enumerate(infile):
                    if f.endswith(".c") or f.endswith(".cpp") or f.endswith(".java") or f.endswith(".cs"):
                        if pattern_cfunc.match(line) or pattern_class.match(line) or pattern_func.match(line) or pattern_public.match(line) or pattern_private.match(line) or pattern_protected.match(line):
                            # Check if the previous or next several lines are a comment, if yes write them together with the current line to the outfile
                            if i == 0:
                                if ccsjava_pattern1.match(infile[i+1]) or ccsjava_pattern2.match(infile[i+1]):
                                    # Write the current line to the outfile together with the next line
                                    outfile.write(line)
                                    outfile.write(infile[i+1])
                                    break
                            elif i == len(infile):
                                if ccsjava_pattern1.match(infile[i-1]) or ccsjava_pattern2.match(infile[i-1]):
                                    # Write the current line to the outfile together with the previous line
                                    outfile.write(infile[i-1])
                                    outfile.write(line)
                                    break
                            else:
                                if ccsjava_pattern1.match(infile[i-1]) or ccsjava_pattern2.match(infile[i-1]):
                                    # Write the current line to the outfile together with the previous line
                                    outfile.write(infile[i-1])
                                    outfile.write(line)
                                    break
                                elif ccsjava_pattern1.match(infile[i+1]) or ccsjava_pattern2.match(infile[i+1]):
                                    # Write the current line to the outfile together with the next line
                                    outfile.write(line)
                                    outfile.write(infile[i+1])
                                    break

                    elif f.endswith(".py"):
                        if pattern_class.match(line) or pattern_func.match(line):
                            # Check if the previous or next several lines are a comment, if yes write them together with the current line to the outfile
                            if i == 0:
                                if python_pattern1.match(infile[i+1]) or python_pattern2.match(infile[i+1]) or python_pattern3.match(infile[i+1]):
                                    # Write the current line to the outfile together with the next line
                                    outfile.write(line)
                                    outfile.write(infile[i+1])
                                    break
                            elif i == len(infile):
                                if python_pattern1.match(infile[i-1]) or python_pattern2.match(infile[i-1]) or python_pattern3.match(infile[i-1]):
                                    # Write the current line to the outfile together with the previous line
                                    outfile.write(infile[i-1])
                                    outfile.write(line)
                                    break
                            else:
                                if python_pattern1.match(infile[i-1]) or python_pattern2.match(infile[i-1]) or python_pattern3.match(infile[i-1]):
                                    # Write the current line to the outfile together with the previous line
                                    outfile.write(infile[i-1])
                                    outfile.write(line)
                                    break
                                elif python_pattern1.match(infile[i+1]) or python_pattern2.match(infile[i+1]) or python_pattern3.match(infile[i+1]):
                                    # Write the current line to the outfile together with the next line
                                    outfile.write(line)
                                    outfile.write(infile[i+1])
                                    break

if __name__ == "__main__":

    if dataset_name == "codeparrot":
        source_dir, meta_csv = source_codeparrot(prompt_num)
    elif dataset_name == "thepile":
        source_dir, meta_csv = source_thepile(prompt_num)
    elif dataset_name == "gcpy":
        source_dir, meta_csv = source_gcpy(prompt_num)

    prompt_dataset(source_dir)