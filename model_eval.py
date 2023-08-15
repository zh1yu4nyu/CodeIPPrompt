import os
import sys
import csv
import pandas as pd
import datetime
import difflib
import subprocess
from jplag import jplag_score_func


# Check two programs and return similarity scores
def check_file(test, source, language):

    match_results = "match_" + test.split("/")[-1].split(".")[0] + ".txt"
    subprocess.call("node dolos_match.js " + test + " " + source + " > " + match_results, shell=True)

    file_extension = test.split(".")[-1]
    temp_matched = "temp." + file_extension

    dolos_score = 0
    jplag_score = 0

    if os.stat(match_results).st_size == 0:
        print("No matched code snippets")

    else:
        with open(match_results, "r") as f:
            for line in f:
                start_line_number = line.split("matches with")[1].split("}")[0].split("{")[1].split(",")[0] 
                end_line_number = line.split("matches with")[1].split("}")[0].split("{")[1].split(",")[1].split("->")[1].replace(" ", "") 
                start_line_number = str(int(start_line_number) + 1)
                end_line_number = str(int(end_line_number) + 1)
                # Use sed to get the matched code snippets
                subprocess.call(["sed", "-n", start_line_number + "," + end_line_number + "p", source], stdout=open(temp_matched, "a"))
        
        dolos_result = subprocess.run(["node", "dolos_score.js", test, temp_matched], stdout=subprocess.PIPE)
        try:
            dolos_score = dolos_result.stdout.decode().split("Similarity: ")[1].replace("\n", "")
        except:
            dolos_score = 0
        try:
            jplag_score = jplag_score_func(test, temp_matched, language)
        except:
            jplag_score = 0

    subprocess.call("rm -rf " + temp_matched, shell=True)
    subprocess.call("rm -rf " + match_results, shell=True)

    return dolos_score, jplag_score


def program_diff(test, test_subdir, prompt):
    
    temp_dir = "Programs_Cleaned/" + test_subdir
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    temp_test = temp_dir + "/" + test.split("/")[-1]

    # Read the contents of the two programs into variables
    program1 = open(test).read()
    program2 = open(prompt).read()

    # Create a Differ object
    differ = difflib.Differ()

    # Use the compare function to compare the two programs and get the difference
    diff = list(differ.compare(program1.splitlines(keepends=True), program2.splitlines(keepends=True)))

    # Iterate over the difference and find the lines that are common to both programs
    common_lines = []
    for line in diff:
        if line.startswith(' '):
            common_lines.append(line[2:])

    # Remove the common lines from program1
    program1 = program1.splitlines(keepends=True)
    for line in common_lines:
        program1.remove(line)

    # Write the modified program1 back to the file
    with open(temp_test, 'w') as f:
        f.writelines(program1)


if __name__ == "__main__":

    start_time = datetime.datetime.now()
    
    # Check if the user has provided the correct number of arguments
    if len(sys.argv) != 2:
        print("Usage: python3 model_eval.py <test_path>")
        sys.exit(1)

    test_subdir = sys.argv[1]
    model_name = test_subdir.split("_")[0]
    source_subdir = test_subdir.replace(model_name, "source")
    prompt_subdir = test_subdir.replace(model_name, "prompts")
    time_stamp = test_subdir.split("_")[-1]

    meta_path = "Source/" + source_subdir + "/" + "meta_" + time_stamp + ".csv"

    result_path = "Results/results_" + model_name + "_" + prompt_subdir.split("_")[1] + "_" + prompt_subdir.split("_")[2] + ".csv"
    
    with open(meta_path, "r") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            repo_name = row[0]
            file_path = row[1]
            license = row[2]
            language = row[3]

            if "/" in file_path:
                file_name = file_path.split("/")[-1]
            else:
                file_name = file_path

            file_extension = file_name.split(".")[-1]
            
            source_file = "Source/" + source_subdir + "/" + file_name
            prompt_file = "Prompts/" + prompt_subdir + "/" + file_name

            if os.path.exists(result_path):
                df = pd.read_csv(result_path)
                if source_file in df.iloc[:, 0].values:
                    print(source_file + " is already in " + result_path)
                    continue

            highest_score = 0
            highest_content = [source_file, file_name, 0, 0, 0, 0]
            
            # Test files are filename_n.py, where n is 0 to 9
            for i in range(10):
                test_file = "Programs/" + test_subdir + "/" + file_name.split(".")[0] + "_" + str(i) + "." + file_extension
                
                if not os.path.exists(test_file):
                    print("Test file does not exist: " + test_file)
                    continue

                # If test file is empty, skip it
                if os.stat(test_file).st_size == 0:
                    print("Test file is empty: " + test_file)
                    continue

                # If test path contains special characters, skip it
                if " " in test_file or "$" in test_file:
                    print("Test file contains space or $: " + test_file)
                    continue
                if any(u'\u4e00' <= c <= u'\u9fff' for c in test_file):
                    print("Test file contains special characters: " + test_file)
                    continue

                file_extension = file_name.split(".")[-1]
                if file_extension == 'py':
                    language = 'python'
                elif file_extension == 'java':
                    language = 'java'
                elif file_extension == 'cs':
                    language = 'csharp'
                elif file_extension == 'cpp' or file_extension == 'c':
                    language = 'cpp'

                dolos_score, jplag_score = check_file(test_file, source_file, language)

                program_diff(test_file, test_subdir, prompt_file)
                test_clean = "Programs_Cleaned/" + test_subdir + "/" + file_name
                dolos_score_clean, jplag_score_clean = check_file(test_clean, source_file, language)

                file_highest = max(float(dolos_score_clean), float(jplag_score_clean))
                if file_highest > float(highest_score):
                    highest_score = file_highest
                    highest_content = [source_file, file_name, dolos_score, jplag_score, dolos_score_clean, jplag_score_clean]

            # If the content is not empty, write it to the result file
            if highest_content:
                with open(result_path, "a") as f:
                    writer = csv.writer(f)
                    if os.stat(result_path).st_size == 0:
                        writer.writerow(["source_file", "file_name", "dolos_score", "jplag_score", "dolos_score_clean", "jplag_score_clean"])
                    writer.writerow(highest_content)

    end_time = datetime.datetime.now()

    # Print the time taken in hour-minute-second format
    elapsed_time = end_time - start_time
    print("Time taken: " + str(elapsed_time))

# Delete the temporary files
subprocess.call("rm -rf Programs_Cleaned", shell=True)