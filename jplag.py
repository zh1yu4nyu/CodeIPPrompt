import os
import subprocess

def jplag_score_func(test, source, language):

    jplag_score = 0

    if not os.path.exists("jplag_test_dir"):
        subprocess.call("mkdir -p jplag_test_dir", shell=True)
    subprocess.call("cp " + test + " jplag_test_dir", shell=True)

    if not os.path.exists("jplag_source_dir"):
        subprocess.call("mkdir -p jplag_source_dir", shell=True)
    subprocess.call("cp " + source + " jplag_source_dir", shell=True)

    if language == "cpp":
        flag_l = "cpp"
    elif language == "python":
        flag_l = "python3"
    elif language == "java":
        flag_l = "java"
    elif language == "csharp":
        flag_l = "csharp"
        
    test = "jplag_test_dir"
    source = "jplag_source_dir"
    
    command = "java -jar jplag-4.1.0-jar-with-dependencies.jar -l " + flag_l + " -r " + "jplag_results" + " -new " + test + " -old " + "jplag_source_dir" + " > jplag_output.txt"

    try:
        subprocess.call(command, shell=True)
    except OSError as e:
        print("Error: " + str(e))

    with open("jplag_output.txt", "r") as file:
        for line in file:
            if "Comparing jplag_test_dir" in line:
                jplag_score = float(line.split(":")[3].replace(" ", ""))

    # Delete the temporary files
    subprocess.call("rm -rf jplag_test_dir", shell=True)
    subprocess.call("rm -rf jplag_source_dir", shell=True)
    subprocess.call("rm -rf jplag_output.txt", shell=True)
    subprocess.call("rm -rf " + "jplag_results" + "_unzip", shell=True)
    subprocess.call("rm -rf " + "jplag_results" + ".zip", shell=True)

    return jplag_score