from pydub import AudioSegment
from os import listdir
from os.path import isfile, join
import re

class Stitch:
    def __init__(self):
        self.path = "../export/audio/"
        self.bookname = "book"
        self.clip_path =  self.path + "audio_clips/"
        print("Stitching audio clips")

    def stitchAudio(self):
        files = self.ls()
        if files:
            print(files)
            root = AudioSegment.from_file(self.clip_path + files[0])
            for file in files[1:]:
                audioToAppend = AudioSegment.from_file(self.clip_path + file)
                root += audioToAppend

            root.export(f"{self.path}render/{self.bookname}_export.mp3", format="mp3")
            print("Finished Stitching...")
        else:
            print("Couldn't find files")


    def ls(self):
        files = [f for f in listdir(self.clip_path) if isfile(join(self.clip_path, f))]
        files_sorted = sorted(files, key=lambda x: int(re.search(r'^(\d+)_', x).group(1)))
        return files_sorted
