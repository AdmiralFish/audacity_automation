import pipe_test as pipe
from data import cwd, set_a, set_a_names, set_b, set_b_names, export_dir_empty
import json

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
    
def import_track(file):
    pipe.do_command(f'Import2: Filename="{file}"')

def trunc_silence():
    pipe.do_command('SelectAll:')
    pipe.do_command('TruncateSilence: Minimum=0.2 Truncate=0.0 Independent=True')

def get_track_data():
    track_info = json.loads(pipe.do_command("GetInfo: Type=Tracks").replace("BatchCommand finished: OK", ''))
    try:
        t1_info = track_info.pop(0)
        t2_info = track_info.pop(0)
    except IndexError():
        print("ERROR: No tracks loaded into audacity.")
    return t1_info, t2_info

def equal_length():
    if track1.length < track2.length:
        long_track = track2
        short_track = track1
    else:
        long_track = track1
        short_track = track2

    timeshift = 100 - ((short_track.length / long_track.length) * 100)
    
    pipe.do_command('SelectAll:')
    pipe.do_command(f'SelectTracks: Mode="Set" Track="{short_track.id}" TrackCount="1"')
    pipe.do_command(f'ChangeSpeed: Percentage={-(timeshift)}') 

    short_track.length = long_track.length

def add_silence():
    for track in [track1, track2]:
        # Adds silence at start and end by copy/repeat/silence a slice of audio.
        pipe.do_command(f'Select: Start="0" End="1" Track={track.id} Mode="Set" RelativeTo="ProjectStart"')
        pipe.do_command('Repeat:Count="1"')
        pipe.do_command('SelectTime: Start="0" End="1" RelativeTo="SelectionStart"')
        pipe.do_command('Silence:')

        pipe.do_command(f'Select: Start="0" End="1" Track={track.id} Mode="Set" RelativeTo="ProjectEnd"')
        pipe.do_command('Repeat:Count="1"')
        pipe.do_command('SelectTime: Start="0" End="1" RelativeTo="ProjectEnd"')
        pipe.do_command('Silence:')

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
    t1_dic, t2_dic = get_track_data()
    global track1, track2
    track1 = Track(t1_dic, '0')
    track2 = Track(t2_dic, '1')

    # Equalize length of both tracks by slowing the faster track. 
    equal_length()

    # Add 1 sec of silence to either side.
    add_silence()
    
    # Export files as WAV tracks and Audacity projects.
    export_files()

    # Removes old tracks from project ready for next parse.
    cleanup()

if export_dir_empty == False:
    print("Either 'exported_files' or 'exported_projects' is not empty - please remove files to avoid overwriting!")
    
elif set_a == [] or set_b == []:
    print("Either set_a or set_b directories are empty - please add tracks to be combined!")
    
else:
    for file_number in range(len(set_a)):
        main()
    print("\n\n All files succesfully merged!")

