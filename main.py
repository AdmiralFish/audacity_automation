import pipe_test as pipe
from data import cwd, set_a, set_a_names, set_b, set_b_names, export_dir_empty, white_noise_path
import json, csv

class Track:
    def __init__(self, track_info_dict, id):
        self.length = float(track_info_dict['end'])
        self.id = id    
        if self.id == '0':
            self.name = set_a_names[file_number]
        else:
            self.name = set_b_names[file_number]
        pipe.do_command(f'SelectTracks: Mode=Set Track={self.id} TrackCount=1')
        pipe.do_command(f'SetTrackStatus: Name={self.name}')
        self.data = [self.name, self.id, self.length]
    
def import_track(file):
    pipe.do_command(f'Import2: Filename="{file}"')

def trunc_silence():
    pipe.do_command('SelectAll:')
    pipe.do_command('TruncateSilence: Minimum=0.2 Truncate=0.0 Independent=True')

def get_track_data(track_number):
    track_info = json.loads(pipe.do_command("GetInfo: Type=Tracks").replace("BatchCommand finished: OK", ''))
    try:
        t_info = track_info.pop(track_number)
    except IndexError():
        print("ERROR: That track does not exist.")
    return t_info

def add_silence(seconds, tracks_list):
    for track in tracks_list:
        # Adds silence at start and end by copy/repeat/silence a slice of audio.
        pipe.do_command(f'Select: Start="0" End="{seconds}" Track={track.id} Mode="Set" RelativeTo="ProjectStart"')
        pipe.do_command('Repeat:Count="1"')
        pipe.do_command(f'SelectTime: Start="0" End="{seconds}" RelativeTo="SelectionStart"')
        pipe.do_command('Silence:')

        pipe.do_command(f'Select: Start="0" End="{seconds}" Track={track.id} Mode="Set" RelativeTo="ProjectEnd"')
        pipe.do_command('Repeat:Count="1"')
        pipe.do_command(f'SelectTime: Start="0" End="{seconds}" RelativeTo="ProjectEnd"')
        pipe.do_command('Silence:')

def allign_tracks():
    if track1.length < track2.length:
        l_track = track2
        s_track = track1
    else:
        l_track = track1
        s_track = track2

    shift = (l_track.length - s_track.length) / 2
    add_silence(shift, [s_track])

def add_white_noise():
    # Needs cleaing up
    if track1.length < track2.length:
        l_track = track2
    else:
        l_track = track1

    import_track(white_noise_path)
    white_noise = Track(get_track_data(2), '2')  
    trim = white_noise.length - (l_track.length +2 )
    pipe.do_command(f'Select: Start="0" End="{trim}" Track={white_noise.id} Mode="Set" RelativeTo="ProjectEnd"')
    pipe.do_command('Delete:')


def export_files():
    pipe.do_command(f'SaveProject2: Filename="{cwd}\\exported_projects\\{track1.name}_&_{track2.name}_project.aup"')
    pipe.do_command('SelectAll:')
    pipe.do_command(f'Export2: Filename="{cwd}\\exported_files\\{track1.name}_&_{track2.name}.wav"')
    print(f"File {track1.name}_&_{track2.name} exported successfully.")

def cleanup():
    pipe.do_command('SelectAll:')
    pipe.do_command('RemoveTracks')

def main():
    # Imports tracks from both directories.
    import_track(set_a[file_number])
    import_track(set_b[file_number])

    # Trim silence from either side of both tracks.
    trunc_silence()
    
    # Get track data and import into Python objects. 
    t1_dic, t2_dic = get_track_data(0), get_track_data(1)
    global track1, track2
    track1 = Track(t1_dic, '0')
    track2 = Track(t2_dic, '1')

    # Write data to CSV file.
    with open('OutputInfo.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        for track in [track1, track2]:
            writer.writerow(track.data)

    # Align tracks to their midpoint.
    allign_tracks()

    # Add 1 sec of silence to either side of both tracks.
    add_silence(1, [track1, track2])
    
    # Add white noise.
    add_white_noise()

    # Export files as WAV tracks and Audacity projects.
    export_files()

    # Removes old tracks from project ready for next parse.
    cleanup()

# Creates CSV file with output data.
with open('OutputInfo.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Name", "Set", "Duration"])

# Run script with error handling.
if export_dir_empty == False:
    print("ERROR: Either 'exported_files' or 'exported_projects' is not empty - please remove files to avoid overwriting!")
    
elif set_a == [] or set_b == []:
    print("ERROR: Either set_a or set_b directories are empty - please add tracks to be combined!")

elif len(set_a) != len(set_a):
    print("ERRPR: Uneven amount of files in set_a & set_b!")

else:
    for file_number in range(len(set_a)):
        main()
    print("\n\n All files succesfully merged!")

