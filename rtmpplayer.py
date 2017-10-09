#!/home/tommy/anaconda3/bin/python3.6

import librtmp, sys, time, os
from pydub import AudioSegment

path = "/home/pi/hdd/Radio/"
os.chdir(path)

filename = str(time.localtime().tm_year) + str(time.localtime().tm_mon) + str(time.localtime().tm_mday) + "_" + sys.argv[1]
flv_name = filename + ".flv"
mp3_name = filename + ".mp3"

conn = librtmp.RTMP("rtmp://ebsonair.ebs.co.kr/fmradiofamilypc/familypc1m ", live=True)

try:
    print("Connecting...")
    conn.connect()
except RTMPError:
    print("Connection failed\n")
    sys.exit()

print("Connected")
start_time = time.localtime()

try:
    stream = conn.create_stream()
except RTMPError:
    print("Stream create fail")
    stream.close()
    conn.close()
print("Created stream")


with open(flv_name, "wb") as f:
    while True:
        try:
            data = stream.read(1024 * 1024)
            f.write(data)
            cur_time = time.localtime()
            
            if cur_time.tm_min - start_time.tm_min >= 1:
                break

        except IOError:
            break

print("Finished filed writing")
stream.close()
conn.close()
f.close()

print("Converting...")
raw = AudioSegment.from_flv(flv_name)
raw.export(mp3_name, format="mp3")
print("Converted")

os.remove(flv_name)
print("Deleted flv")
