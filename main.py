import pipe_test as p
import json


# Removes sub-string from output - converts to Python Dict
def get_track_data():
    try:
        track_info = json.loads(p.do_command("GetInfo: Type=Tracks").replace("BatchCommand finished: OK", ''))
    except IndexError():
        print("No tracks loaded into audacity.")

    track1 = track_info.pop(0)
    track2 = track_info.pop(0)

# Base logic to normalize track length 
## Need to change into function still!
track1_end = float(track1['end'])
track2_end = float(track2['end'])

timeshift = 100 - ((track1_end / track2_end) * 100)

p.do_command(f'ChangeSpeed: Percentage={-(timeshift)}') # Still not 100% accurate?

# def shorter_track():

get_track_data()

"""
Scratchpad

"""

# do_command("Import2: Filename=C:/Users/tompe/Desktop/Raw_Audio.mp3")

# san_string = do_command("GetInfo: Type=Tracks").translate({ord(i): None for i in '[]'})
# print(san_string)

# san_lst = san_string.split('{')
# print(san_lst)

# track_info = ast.literal_eval(do_command("GetInfo: Type=Tracks").pop())


# track_info = [ast.literal_eval(data) for data in do_command("GetInfo: Type=Tracks")]
# print(track_info, type(track_info))
