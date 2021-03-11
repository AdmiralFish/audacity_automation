import json, csv
import pipe_test as pipe

class Project:
    def __init__(self):
        self.tracks = {}

    def import_track(self, file, trunc_silence=True):
        track_id = len(self.tracks)
        pipe.do_command(f'Import2: Filename="{file}"')
        json_info = json.loads(pipe.do_command("GetInfo: Type=Tracks").replace("BatchCommand finished: OK", ''))
        dic = json_info.pop(track_id)

        self.tracks[track_id] = Track(dic, track_id)
        



class Track:
    def __init__(self, track_info, id, name=track_info['name']):
        self.length = float(track_info_dict['end'])
        self.id = id    
        self.name = name
        pipe.do_command(f'SelectTracks: Mode=Set Track={self.id} TrackCount=1')
        pipe.do_command(f'SetTrackStatus: Name={self.name}')
        self.data = [self.name, self.id, self.length]

    def rename(self, new_name):
