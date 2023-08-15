import re
import os
import sys
import csv
import datetime


def prompts_github(license, language):

    if language == "cpp":
        language_dir = "C++"
        file_extension = "cpp"
    elif language == "python":
        language_dir = "Python"
        file_extension = "py"
    elif language == "java":
        language_dir = "Java"
        file_extension = "java"
    elif language == "csharp":
        language_dir = "C#"
        file_extension = "cs"

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

    source_dir = "./Licensed_code/" + license + "/" + language_dir + "/"

    now_time = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

    # Make a directory to store the prompts and metadata
    prompt_dir = "Prompts/prompts_" + license + "_" + language + "_" + now_time
    source_save_dir = "Source/source_" + license + "_" + language + "_" + now_time
    os.mkdir(prompt_dir)
    os.mkdir(source_save_dir)

    meta_path = source_save_dir + "/" + "meta_" + now_time + ".csv"

    # write header to the metadata file, named repo_name,path,license,language
    with open(meta_path, "w") as f:
        writer = csv.writer(f)
        writer.writerow(["repo_name", "path", "license", "language"])
        f.close()

    # Get the number of repository folders in the source_dir
    total_num_repos = len(os.listdir(source_dir))
    current_num_repos = 0
    
    # Loop through each subdirectory only in the source directory
    for repo in os.listdir(source_dir):
        current_num_repos += 1
        if current_num_repos % 1000 == 0:
            print("Current number of repos: " + str(current_num_repos) + "/" + str(total_num_repos))
        repo_path = os.path.join(source_dir, repo)
        if os.path.isdir(repo_path):
            # Inside a repository, read files with the extension one by one
            for subdir_path, _, files in os.walk(repo_path):
                
                for f in files:

                    # Check if it is a file, if the file ends with the extension and if it does not include Chinese characters
                    if os.path.isfile(os.path.join(subdir_path, f)) and f.endswith(file_extension) and not any(u'\u4e00' <= c <= u'\u9fff' for c in f):
                        
                        file_path = os.path.join(subdir_path, f)
                        # Write information to the metadata file
                        with open(meta_path, "a") as meta_writer:
                            writer = csv.writer(meta_writer)
                            writer.writerow([repo, os.path.relpath(file_path, repo_path), license, language_dir])
                            meta_writer.close()
                        
                        # Save the source code to the source_save_dir
                        infile_save_path = source_save_dir + "/" + f
                        with open(file_path, "r") as source_path, open(infile_save_path, "w") as infile_save_path:
                            try:
                                source_path_content = source_path.read()
                                infile_save_path.write(source_path_content)
                            except UnicodeDecodeError:
                                continue
                        
                        prompt_path = prompt_dir + "/" + f

                        with open(file_path, "r") as infile, open(prompt_path, "w") as outfile:
                
                            try:
                                infile = infile.readlines()
                            except UnicodeDecodeError:
                                continue
                            num_lines = len(infile)
                            if num_lines < 2:
                                continue
                            # Loop through the line number of infile
                            for i, line in enumerate(infile):
                                if f.endswith(".c") or f.endswith(".cpp") or f.endswith(".java") or f.endswith(".cs"):
                                    if pattern_cfunc.match(line) or pattern_class.match(line) or pattern_func.match(line) or pattern_public.match(line) or pattern_private.match(line) or pattern_protected.match(line):
                                        # Check if the previous or next several lines are a comment, if yes write them together with the current line to the outfile
                                        if i == 0:
                                            if ccsjava_pattern1.match(infile[i+1]) or ccsjava_pattern2.match(infile[i+1]):
                                                if not any(c in '|<>"*?:/ ' for c in infile[i+1]) or any(ord(c) > 127 for c in infile[i+1]) or any(u'\u4e00' <= c <= u'\u9fff' for c in infile[i+1]):
                                                    # Write the current line to the outfile together with the next line
                                                    outfile.write(line)
                                                    outfile.write(infile[i+1])
                                                    break
                                        elif i == (num_lines-1):
                                            if ccsjava_pattern1.match(infile[i-1]) or ccsjava_pattern2.match(infile[i-1]):
                                                if not any(c in '|<>"*?:/ ' for c in infile[i-1]) or any(ord(c) > 127 for c in infile[i-1]) or any(u'\u4e00' <= c <= u'\u9fff' for c in infile[i-1]):
                                                    # Write the current line to the outfile together with the previous line
                                                    outfile.write(infile[i-1])
                                                    outfile.write(line)
                                                    break
                                        else:
                                            if ccsjava_pattern1.match(infile[i-1]) or ccsjava_pattern2.match(infile[i-1]):
                                                if not any(c in '|<>"*?:/ ' for c in infile[i-1]) or any(ord(c) > 127 for c in infile[i-1]) or any(u'\u4e00' <= c <= u'\u9fff' for c in infile[i-1]):
                                                    # Write the current line to the outfile together with the previous line
                                                    outfile.write(infile[i-1])
                                                    outfile.write(line)
                                                    break
                                            elif ccsjava_pattern1.match(infile[i+1]) or ccsjava_pattern2.match(infile[i+1]):
                                                if not any(c in '|<>"*?:/ ' for c in infile[i+1]) or any(ord(c) > 127 for c in infile[i+1]) or any(u'\u4e00' <= c <= u'\u9fff' for c in infile[i+1]):
                                                    # Write the current line to the outfile together with the next line
                                                    outfile.write(line)
                                                    outfile.write(infile[i+1])
                                                    break

                                elif f.endswith(".py"):
                                    if pattern_class.match(line) or pattern_func.match(line):
                                        # Check if the previous or next several lines are a comment, if yes write them together with the current line to the outfile
                                        if i == 0:
                                            if python_pattern1.match(infile[i+1]) or python_pattern2.match(infile[i+1]) or python_pattern3.match(infile[i+1]):
                                                if not any(c in '|<>"*?:/ ' for c in infile[i+1]) or any(ord(c) > 127 for c in infile[i+1]) or any(u'\u4e00' <= c <= u'\u9fff' for c in infile[i+1]):
                                                    # Write the current line to the outfile together with the next line
                                                    outfile.write(line)
                                                    outfile.write(infile[i+1])
                                                    break
                                        elif i == (num_lines-1):
                                            if python_pattern1.match(infile[i-1]) or python_pattern2.match(infile[i-1]) or python_pattern3.match(infile[i-1]):
                                                if not any(c in '|<>"*?:/ ' for c in infile[i-1]) or any(ord(c) > 127 for c in infile[i-1]) or any(u'\u4e00' <= c <= u'\u9fff' for c in infile[i-1]):
                                                    # Write the current line to the outfile together with the previous line
                                                    outfile.write(infile[i-1])
                                                    outfile.write(line)
                                                    break
                                        else:
                                            if python_pattern1.match(infile[i-1]) or python_pattern2.match(infile[i-1]) or python_pattern3.match(infile[i-1]):
                                                if not any(c in '|<>"*?:/ ' for c in infile[i-1]) or any(ord(c) > 127 for c in infile[i-1]) or any(u'\u4e00' <= c <= u'\u9fff' for c in infile[i-1]):
                                                    # Write the current line to the outfile together with the previous line
                                                    outfile.write(infile[i-1])
                                                    outfile.write(line)
                                                    break
                                            elif python_pattern1.match(infile[i+1]) or python_pattern2.match(infile[i+1]) or python_pattern3.match(infile[i+1]):
                                                if not any(c in '|<>"*?:/ ' for c in infile[i+1]) or any(ord(c) > 127 for c in infile[i+1]) or any(u'\u4e00' <= c <= u'\u9fff' for c in infile[i+1]):
                                                    # Write the current line to the outfile together with the next line
                                                    outfile.write(line)
                                                    outfile.write(infile[i+1])
                                                    break

                        # If the outfile is empty, delete it
                        if os.stat(prompt_path).st_size == 0:
                            os.remove(prompt_path)

if __name__ == "__main__":

    license = sys.argv[1]
    language = sys.argv[2] 

    prompts_github(license, language)