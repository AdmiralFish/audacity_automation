import json
import path_builder as pb
import pipe_test as pipe

class Project:
    def __init__(self):
        self.tracks = {}
        self.name = ""
        self.end = None

    def __iter__(self):
        return iter([self.tracks[x] for x in range(len(self.tracks))])
        
    def import_track(self, file, name=False, strip=False):
        track_index = len(self.tracks)
        pipe.do_command(f'Import2: Filename="{file}"')
        if strip:
            self.strip_silence()
        track_info = json.loads(pipe.do_command("GetInfo: Type=Tracks").replace("BatchCommand finished: OK", '')).pop(track_index)
        self.tracks[track_index] = Track(track_info, track_index, name)
        return track_index

    def strip_silence(self):
        pipe.do_command('SelectAll:')
        pipe.do_command('TruncateSilence: Minimum=0.2 Truncate=0.0 Independent=True')
    
    def sort_tracks(self, reverse, sorter): # Sorter is lambda function 
        ls = [track for track in self]
        ls.sort(reverse=reverse, key=sorter)
        return ls

    def allign_tracks(self):
        sorted_tracks = self.sort_tracks(True, lambda x: x.length)
        longest_track = sorted_tracks.pop(0)
        for track in sorted_tracks:
            shift = (longest_track.length - track.length) / 2
            track.add_silence_both(shift)

    def update_end(self):
        track_info = json.loads(pipe.do_command("GetInfo: Type=Tracks").replace("BatchCommand finished: OK", ''))
        track_info.sort(reverse=True, key = lambda x: x['end'])
        self.end = track_info.pop(0)['end']

    def add_whitenoise(self):
        self.update_end()
        wn = self.import_track(pb.input_files["white noise"], name="White Noise")
        trim = self.tracks[wn].length - self.end
        pipe.do_command(f'Select: Start="0" End="{trim}" Track={wn} Mode="Set" RelativeTo="ProjectEnd"')
        pipe.do_command('Delete:')

    def export(self, exp_prj=False):
        if exp_prj:
            pipe.do_command(f'SaveProject2: Filename="{pb.output_dir}\\project_files\\{self.name}_project.aup"')
        pipe.do_command('SelectAll:')
        pipe.do_command(f'Export2: Filename="{pb.output_dir}\\merged_audio\\{self.name}.wav"')

    def cleanup(self):
        pipe.do_command('SelectAll:')
        pipe.do_command('RemoveTracks')

class Track:
    def __init__(self, track_info, index, name=False):
        self.length = float(track_info['end'])
        self.index = index
        if name:
            self.name = name
        else:
            self.name = f"{set_name}{str(file_number+1).zfill(3)}"
        self.info = [self.name, self.index, self.length]

        self.select()
        pipe.do_command(f'SetTrackStatus: Name={self.name}')
    
    def __repr__(self):
        return self.name

    def select(self, mode='Set'):
        pipe.do_command(f'SelectTracks: Mode={mode} Track={self.index} TrackCount=1')

    def add_silence(self, seconds, position1, position2): # Position = "ProjectStart", "ProjectEnd", "SelectionStart"
        pipe.do_command(f'Select: Start="0" End="{seconds}" Track={self.index} Mode="Set" RelativeTo={position1}')
        pipe.do_command('Repeat:Count="1"')
        pipe.do_command(f'SelectTime: Start="0" End="{seconds}" RelativeTo={position2}')
        pipe.do_command('Silence:')

    def add_silence_both(self, seconds):
        self.add_silence(seconds, "ProjectStart", "SelectionStart")
        self.add_silence(seconds, "ProjectEnd", "ProjectEnd")

# Arguments = 'strip', 'align', 'buffer', 'white', 'exp_prj'
def main(*args):
    project = Project()
    # Imports track[x] from each input directory.
    global set_name
    for set_name in pb.input_sets:
        if 'strip' in args:
            project.import_track(pb.get_file_path(set_name, file_number), strip=True)
        else:
            project.import_track(pb.get_file_path(set_name, file_number))

    for name in [track.name for track in project]:
        project.name += (name+'_')

    for track in project:
        pb.csv_writer('a', track.info)

    if 'align' in args:
        project.allign_tracks()

    if 'buffer' in args:
        for track in project:
            track.add_silence_both(1)
    
    if 'white' in args:
        project.add_whitenoise()
    
    if 'exp_prj' in args:
        project.export(exp_prj=True)
    else:
        project.export()
    
    project.cleanup()
    
if __name__ == '__main__':
    for file_number in range(pb.total_files):
        main('strip', 'align', 'buffer', 'white', 'exp_prj')

    
    
