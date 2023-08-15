# This is an example script that uses CodeParrot to generate programs for a given set of prompts.
# model options: codeparrot/codeparrot, codeparrot/codeparrot-small

from transformers import pipeline
import os
import sys
from datetime import datetime


def codeparrot(prompt, model_name, output_path):
    os.environ['HF_HOME'] = <Your_Env_Variable_Path>
    pipe = pipeline("text-generation", model=model_name, pad_token_id = 50256, device = 1)
    outputs = pipe(prompt, num_return_sequences=10, max_length = 256)
    output_programs = []
    for item in outputs:
        if "generated_text" in item:
            output_programs.append(item["generated_text"])
    for i in range(10):
        output_file = output_path.split('.')[0] + "_" + str(i) + "." + output_path.split('.')[1]
        with open(output_file, 'w') as f:
            f.write(output_programs[i])


if __name__=='__main__':

    start_time = datetime.now()

    model_name = sys.argv[1]
    prompt_folder = sys.argv[2]

    if model_name == "codeparrot/codeparrot":
        model = "CodeParrot"
    elif model_name == "codeparrot/codeparrot-small":
        model = "CodeParrotSmall"
    else:
        print("Usage: python3 Example_Parrot.py codeparrot/codeparrot <prompt_folder> OR python3 Example_Parrot.py codeparrot/codeparrot-small <prompt_folder>")
        exit(1)
    root_path = <Your_Root_Path>
    prompt_path = root_path + "Prompts" + "/" + prompt_folder + "/"
    program_path = root_path + "Programs" + "/" + prompt_folder.replace("prompts", model) + "/"
    if not os.path.exists(program_path):
        os.makedirs(program_path)
    # Loop over the programs in the path
    for filename in os.listdir(prompt_path):
        # Open the file that ends with ".py"
        if filename.endswith(".py"):
            output_path = program_path + filename
            output_file_checklast = output_path.split('.')[0] + "_" + "9" + "." + output_path.split('.')[1]
            if os.path.exists(output_file_checklast):
                print(f"{output_file_checklast} already fully generated, continue to next prompt...")
                continue
            # Open the file
            with open(prompt_path + filename, "r") as f:
                print(f"{filename} undergoing generation...")
                # Read the file
                prompt = f.read()
                codeparrot(prompt, model_name, program_path + filename)

    end_time = datetime.now()

    # Calculate the elapsed time
    elapsed_time = end_time - start_time

    # Print the elapsed time in hours, minutes, and seconds
    print(f'Time elapsed: {elapsed_time.days} days, {elapsed_time.seconds//3600} hours, {(elapsed_time.seconds//60)%60} minutes, {elapsed_time.seconds%60} seconds')