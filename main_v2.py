import json, csv
import pipe_test as pipe

class Project:
    def __init__(self):
        self.tracks = {}

    def select_track(self, index, mode='Set'):
        pipe.do_command(f'SelectTracks: Mode={mode} Track={index} TrackCount=1')


    def import_track(self, file, trunc_silence=True):
        track_index = len(self.tracks)
        pipe.do_command(f'Import2: Filename="{file}"')
        json_info = json.loads(pipe.do_command("GetInfo: Type=Tracks").replace("BatchCommand finished: OK", ''))
        dic = json_info.pop(track_id)

        self.tracks[track_index] = Track(dic,)
        
        self.select_track(track_index)
        pipe.do_command(f'SetTrackStatus: Name={self.name}')


class Track:
    def __init__(self, track_info, name=f"{name}{str(file_number).zfill(3)}"):
        self.length = float(track_info['end'])
        self.name = name
        pipe.do_command(f'SelectTracks: Mode=Set Track={self.id} TrackCount=1')
        pipe.do_command(f'SetTrackStatus: Name={self.name}')
        self.data = [self.name, self.id, self.length]