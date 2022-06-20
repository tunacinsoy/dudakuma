import sys
import os
import csv
import multiprocessing as mp
import time

### this script will slice videos with taking input dataset csv and downloaded raw youtube videos should be same dir as with this script
### NOTE edit 'processes=44' field in line71 according to your CPU core number
### make sure ffmpeg executable is in the same directory as with this script and has exec permission OR change the path in line24
count_queue = mp.Queue()

def get_unique_index_string(start_time):
    return start_time.replace(":","").replace(".","")

def get_videofilename_from_url(video_url):
    filename = video_url[len(video_url)-11:]
    return filename + ".mp4"

def cut_raw_video(each_dataset_item):
    vid_filename = get_videofilename_from_url(each_dataset_item['video_url'])
    video_file = "raw_video" + os.sep + vid_filename
    target_video = each_dataset_item['label'] + "_" + vid_filename[:11] + "_" + get_unique_index_string(each_dataset_item['start']) + ".mp4"
    target_video_path = "./" + each_dataset_item['label'] + os.sep + target_video

    if os.path.exists(video_file):
        target_video_path = target_video_path.replace("\\","/")
        video_file = video_file.replace("\\","/")
        #command = "ffmpeg -y -loglevel quiet" + " -i " + video_file + " -ss " + each_dataset_item['start'] +  " -to " + each_dataset_item['end'] + " -c:v libx264 -c:a aac " + target_video_path
        #command = "ffmpeg" + " -i " + video_file + " -ss " + each_dataset_item['start'] +  " -to " + each_dataset_item['end'] + " -c " + target_video_path
        command = "ffmpeg" + " -ss " + each_dataset_item['start'] + " -to " + each_dataset_item['end'] +  " -i " + video_file + " -c copy " + target_video_path
        os.system(command)
    else:
        print("WARNING, video not found: " + video_file)
    
    count_queue.put(1)
    
def counter_worker(queue, size):
    count = 0
    prev = time.time()
    while True:
        item = queue.get() 
        if item is None:
            break
        count += 1
        if count % 150 == 0:
            percent = count/size
            print("{}/{} percent{:.2f} total time: {:.2f}".format(count, size, percent*100, time.time()-prev))
            prev = time.time()

if __name__ == '__main__':
    label_set = set()
    dataset_item_list = []

    with open('./datasets/gecen_sene_dataset.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if row:
                dataset_item = {
                    "video_url": row[0], # TODO change this to videoId
                    "label": row[1],
                    "start": row[2],
                    "end": row[3]
                }
                dataset_item_list.append(dataset_item)
                label_set.add(row[1])

    
    counter_pool = mp.Pool(1, counter_worker,(count_queue, len(dataset_item_list)))
      
    # create label dataset folders
    for each_label in label_set:
        if not os.path.exists(each_label):
            os.makedirs(each_label)
    
    
    with mp.Pool(processes=44) as pool:
        pool.map(cut_raw_video, dataset_item_list)
    
    count_queue.put(None)
    counter_pool.close()
    counter_pool.join()

    print("FINISHED....")
