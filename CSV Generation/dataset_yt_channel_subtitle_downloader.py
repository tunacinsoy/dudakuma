from __future__ import unicode_literals
import requests
from requests.exceptions import HTTPError
import youtube_dl
import sys
import os.path
import re

### Get youtube api key and edit 'api_key' field below
### Edit 'chann_id' field below respective to your selected youtube channel's channel id(it can be extracted through viewving source page of youtube channel in browser)

api_key = "API_KEY"
chann_id = "CHANNEL_ID" # change according to your selected youtube channel

vid_url_list = []

first_run = True
nextpage_tok = ""
request_url = "https://www.googleapis.com/youtube/v3/search?key=" + api_key + "&channelId=" + chann_id + "&part=snippet,id&order=date&maxResults=50"
while(True):
    try:
        if not first_run:
            request_url += "&pageToken=" + nextpage_tok
        response = requests.get(request_url)
        response.raise_for_status()
        # access JSOn content
        if response.status_code == 200:
            jsonResponse = response.json()
            nextpage_tok = jsonResponse["nextPageToken"]
            video_items = jsonResponse["items"]
            if len(video_items) > 0:
                for video in video_items:
                    if video['snippet']['liveBroadcastContent'] == "upcoming":
                        continue
                    vid_item_id = video["id"]
                    vid_item_kind = vid_item_id["kind"]
                    if vid_item_kind == "youtube#video":
                        vid_id = vid_item_id["videoId"]
                        vid_url_list.append(vid_id)
                first_run = False
            else:
                break
    except HTTPError as http_err:
        print(http_err)
        break
    except Exception as err:
        print(err)
        break

chann_vid_list_filename = "CHANNEL_" + chann_id + "_urls.txt"
with open(chann_vid_list_filename, 'w') as f:
    for vid_url_id in vid_url_list:
        f.write("https://www.youtube.com/watch?v=%s\n" % vid_url_id)

for vid_url_id2 in vid_url_list:
    full_vid_url = "https://www.youtube.com/watch?v=" + vid_url_id2
    youtube_dl_options = {"writesubtitles": True, 'skip_download': True, "subtitleslangs": ["tr"], 'forcefilename': True}
    with youtube_dl.YoutubeDL(youtube_dl_options) as ydl2:
        info = ydl2.extract_info(full_vid_url)
        video_filename = ydl2.prepare_filename(info)


print("FINISHED....")
