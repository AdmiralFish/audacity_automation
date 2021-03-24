import json
import path_builder as pb
import pipe_test as pipe

class Project:
    def __init__(self):
        self.tracks = []
        self.name = None
        
    def import_track(self, file, name=None, set_name=None, file_number=None, strip=False):
        track_index = len(self.tracks)
        pipe.do_command(f'Import2: Filename="{file}"')
        track_info = self.get_info(track_index)
        if name == None:
            name = f"{set_name}{str(file_number+1).zfill(3)}"
        track = Track(track_info, track_index, name)
        self.tracks.append(track)
        
        if strip:
            track.strip_silence()
            track.length = self.get_info(track_index)['end']
        return track

    def get_info(self, index=None):
        info = json.loads(pipe.do_command("GetInfo: Type=Tracks").replace("BatchCommand finished: OK", ''))
        if index != None:
            info = info.pop(index)
        return info 

    def allign_tracks(self):
        sorted_tracks = sorted(self.tracks, reverse=True, key=lambda x: x.length)
        longest_track = sorted_tracks.pop(0)
        for track in sorted_tracks:
            shift = (longest_track.length - track.length) / 2
            track.add_silence_both(shift)

    def add_whitenoise(self):
        track_info = self.get_info()
        track_info.sort(reverse=True, key = lambda x: x['end'])
        max_length = track_info.pop(0)['end']

        wn = self.import_track(pb.input_files["white noise"], name="White Noise")
        trim = wn.length - max_length
        pipe.do_command(f'Select: Start="0" End="{trim}" Track={wn.index} Mode="Set" RelativeTo="ProjectEnd"')
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
    def __init__(self, track_info, index, name):
        self.length = float(track_info['end'])
        self.index = index
        self.name = name 
        self.info = [self.name, self.index, self.length]

        self.select()
        pipe.do_command(f'SetTrackStatus: Name="{self.name}"')
    
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

    def strip_silence(self):
        self.select()
        pipe.do_command('TruncateSilence: Minimum=0.2 Truncate=0.0 Independent=True')
    
    def mute(self):
        self.select()
        pipe.do_command(f'MuteTracks:')

# Arguments = 'strip', 'align', 'buffer', 'white', 'exp_prj'
def main(*args):
    for file_number in range(pb.total_files):
        project = Project()
        # Imports track[x] from each input directory.
        for set_name in pb.input_sets:
            if 'strip' in args:
                project.import_track(pb.get_file_path(set_name, file_number), set_name=set_name, file_number=file_number, strip=True)
            else:
                project.import_track(pb.get_file_path(set_name, file_number), set_name=set_name, file_number=file_number)

        project.name = f'audio_control_human{file_number}'
        # for track in project.tracks:
        #     project.name += (track.name+'_')

        for track in project.tracks:
            pb.csv_writer('a', track.info)

        if 'align' in args:
            project.allign_tracks()

        if 'buffer' in args:
            for track in project.tracks:
                track.add_silence_both(1)
        
        if 'white' in args:
            project.add_whitenoise()
        
        if file_number % 2 != 0:
            project.tracks[1].mute()
        else:
            project.tracks[0].mute()

        if 'exp_prj' in args:
            project.export(exp_prj=True)
        else:
            project.export()
        
        project.cleanup()
    
if __name__ == '__main__':
    main('strip', 'align', 'buffer', 'white', 'exp_prj')