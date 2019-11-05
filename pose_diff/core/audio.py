from pydub import AudioSegment

def split_mp3(file_name):
    sound = AudioSegment.from_mp3(file_name)

    halfway_point = len(sound) // 2
    first_half = sound[:halfway_point] + sound[:halfway_point]

    # create a new file "first_half.mp3":
    first_half.export("first_half_twice.mp3", format="mp3")
