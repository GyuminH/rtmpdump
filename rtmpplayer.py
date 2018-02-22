#!/home/tommy/anaconda3/bin/python3.6

import librtmp, sys, time, os
from pydub import AudioSegment

def log(message):
    cur = time.localtime()
    text = str(cur.tm_year) + str(cur.tm_mon) + str(cur.tm_mday) + str(cur.tm_hour) + str(cur.tm_min) + str(cur.tm_sec) + " " + message
    print(text)

path = "/home/pi/hdd/Radio/"
os.chdir(path)

filename = str(time.localtime().tm_year) + str(time.localtime().tm_mon) + str(time.localtime().tm_mday) + "_" + sys.argv[1]
flv_name = filename + ".flv"
mp3_name = filename + ".mp3"
recordTime = int(sys.argv[2]) * 60

conn = librtmp.RTMP("rtmp://ebsonair.ebs.co.kr/fmradiofamilypc/familypc1m ", live=True)

try:
    log("Connecting...")
    conn.connect()
except RTMPError:
    log("Connection failed\n")
    sys.exit()

log("Connected")
start_time = time.time()

try:
    stream = conn.create_stream()
except RTMPError:
    log("Stream create fail")
    stream.close()
    conn.close()
log("Created stream")


with open(flv_name, "wb") as f:
    while True:
        try:
            data = stream.read(1024 * 1024)
            f.write(data)
            cur_time = time.time() 
            
            if cur_time - start_time >= recordTime:
                break

        except IOError:
            break

log("Finished filed writing")
stream.close()
conn.close()
f.close()

log("Converting...")
raw = AudioSegment.from_flv(flv_name)
raw.export(mp3_name, format="mp3")
log("Converted")

os.remove(flv_name)
log("Deleted flv")
