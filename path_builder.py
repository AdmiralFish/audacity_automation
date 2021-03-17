import os, glob, csv

# Paths to script directories.
cwd = os.getcwd()
input_dir = cwd + r"\input"
output_dir = cwd + r"\output"

# Returns a list of all WAV files in a given directory. 
def file_list(directory, ext="wav"):
    return [file.replace("\\", "/") for file in glob.glob(f"{directory}/*.{ext}")]

# Writes to OutputInfo.csv
def csv_writer(mode, data): # Mode = 'w' (write), 'a' (append)
    with open(output_dir + r'\OutputInfo.csv', mode, newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data) # Data must be list

# Check to see if export directoires are empty. 
exp_files = file_list(cwd + r"\output\merged_audio")
exp_proj = file_list(cwd + r"\output\project_files")
if exp_files != [] or exp_proj != []:
    raise Exception("One or both output folders not empty.")

# Creates OutputInfo.csv
csv_writer('w', ["Name", "Set", "Duration"])

# Creating Import File Paths
# List of sub-directory names in 'input'.
input_sets = [dirs for root, dirs, files in os.walk(input_dir)][0]
if len(input_sets) < 2:
    raise Exception("ERROR: Did not detect 2 or more input folders.")

# Stores dict of sub-dict name: file path.
input_files = {}
for set_name in input_sets:
    input_files[set_name] = file_list(f"{input_dir}/{set_name}")
    if set_name == input_sets[0]:
        total_files = len(input_files[set_name])

    if len(input_files[set_name]) != total_files:
        raise Exception("Please ensure all input folders have equal number of tracks.")

# Adds path to white noise file into dict.
input_files["white noise"] = cwd + r"\media\white_noise.wav"

# Gets a file path from input_files dic
def get_file_path(set_name, file_number):
    return input_files[set_name][file_number]

