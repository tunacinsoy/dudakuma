from __future__ import unicode_literals
#from sqlalchemy import null
import youtube_dl
import csv
import os

### this script will download all the youtube videos which are in dataset csv
### edit open("DATASET_CSV_PATH") field in line15 according to your dataset csv file

def get_videofilename_from_url(video_url):
    filename = video_url[len(video_url)-11:]
    return filename + ".mp4"

video_url_set = set()
with open('DATASET_CSV_FILE_PATH') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            line_count += 1
        else:
            if row:
                video_url_set.add(row[0])
                line_count += 1

video_url_list = list(video_url_set)
video_url_not_dw_list = []

for vid in video_url_list:
    vid_file = get_videofilename_from_url(vid)
    if not os.path.exists(os.getcwd() + os.sep + vid_file):
        video_url_not_dw_list.append(vid)
        
ydl_opts = {
    #'format': '135+140/best',
    'format': '135/best',
    'outtmpl': '%(id)s.mp4',
    'noplaylist' : True
}

with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download(video_url_not_dw_list)

print("FINISHED....")
