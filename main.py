import pipe_test as pipe
import json

class Track:
    def __init__(self, track_info_dict, id):
        self.name = track_info_dict['name']
        self.length = float(track_info_dict['end'])
        self.id = id    
    
def import_track(file):
    pipe.do_command(f"Import2: Filename={file}")

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

def equal_length(track1, track2):
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

    print("\n\n Track lengths equalized!")

    short_track.length = long_track.length


def main():
    # for track in track_list:
    #     import_track(track)
    
    trunc_silence()
    
    t1_dic, t2_dic = get_track_data()

    global track1, track2 # FOR TESTING ONLY
    track1 = Track(t1_dic, '0')
    track2 = Track(t2_dic, '1')

    
    equal_length(track1, track2)
 
# TEST BENCH #

test_file1 = 'C:/Users/tompe/Desktop/Raw_Audio.mp3'
test_file2 = 'C:/Users/tompe/Desktop/Raw_Audio2.mp3'

track_list = [test_file1, test_file2]

trunc_silence()


