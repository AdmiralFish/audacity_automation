import os
import glob

def file_list(directory):
    # Returns a list of all WAV files in a given directory. 
    return [file.replace("\\", "/") for file in glob.glob(f"{directory}/*.wav")]


# Creates a list of all WAV files for set_a and set_b. 
cwd = os.getcwd()

# input_sets = 

set_a = file_list(cwd + r"\set_a")
set_b = file_list(cwd + r"\set_b")

white_noise_path = cwd + r"\media\white_noise.wav"


# Labels for naming combined track. 
set_a_names = [f"set_A{str(i).zfill(3)}" for i in range(1, len(set_a)+1)]
set_b_names = [f"set_B{str(i).zfill(3)}" for i in range(1, len(set_b)+1)]


# Check to see if export directoires are empty. 
exp_files = file_list(cwd + r"exported_files")
exp_proj = file_list(cwd + r"exported_projects")
if exp_files or exp_files == []:
    export_dir_empty = True


input_dir = cwd+r"\input"
input_names = [dirs[0] for root, dirs, files in os.walk(input_dir)]
