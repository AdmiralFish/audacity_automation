import os
import glob

def file_list(directory):
    # Returns a list of all WAV files in a given directory. 
    return [file.replace("\\", "/") for file in glob.glob(f"{directory}/*.wav")]

# Links to input folder.
cwd = os.getcwd()
input_dir = cwd + r"\input"

# List of sub-directory names in 'input'.
input_sets = [dirs for root, dirs, files in os.walk(input_dir)][0]
if len(input_sets) < 2:
    raise Exception("ERROR: Did not detect 2 or more input folders.")

# Stores dict of sub-dict name: file path.
input_files = {}
for set_name in input_sets:
    input_files[set_name] = file_list(f"{input_dir}/{set_name}")
# Adds path to white noise file into dict.
input_files["white noise"] = cwd + r"\media\white_noise.wav"

# Labels for naming combined track. 
# set_a_names = [f"set_A{str(i).zfill(3)}" for i in range(1, len(set_a)+1)]
# set_b_names = [f"set_B{str(i).zfill(3)}" for i in range(1, len(set_b)+1)]

# Check to see if export directoires are empty. 
exp_files = file_list(cwd + r"\output\merged_audio")
exp_proj = file_list(cwd + r"\output\project_data")
if exp_files != [] or exp_proj != []:
    raise Exception("One or both output folders not empty.")
