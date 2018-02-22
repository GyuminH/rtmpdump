#!/home/tommy/anaconda3/bin/python3.6

import sys, os, time
from os import listdir
from pathlib import Path
from pydub import AudioSegment

file_ptr = open("log.txt", "a")

def log(message):
    cur = time.localtime()
    text = str(cur.tm_year) + "." + str(cur.tm_mon) + "." + str(cur.tm_mday) + " " + str(cur.tm_hour) + ":" + str(cur.tm_min) + " " + message + "\n"
    file_ptr.write(text)

filelists = listdir()
for f in filelists:
    if ".flv" in f:
        mp3name = f.split('.')[0] + ".mp3"
        log("Converting " + mp3name);
        raw = AudioSegment.from_flv(f)
        raw.export(mp3name)
        my_path = Path("/home/tommy/english/" + mp3name)
        if (my_path.is_file()):
            log("Removing " + f)
            os.remove(f)
