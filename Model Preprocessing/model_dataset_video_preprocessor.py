from json import encoder
from imutils import face_utils
import numpy as np
import imutils
import dlib
import cv2
import os
import argparse
import csv
import multiprocessing as mp
from tqdm import tqdm
import io
from PIL import Image 
import PIL 
import matplotlib.image as mpimg
from matplotlib import pyplot

### this script will do final preprocessing (cutting mouth/lip ares of video frames and append them together into final dataset image)
### edit NUM_PROC=44 field in line144 according to yout CPU core number
### edit open("DATASET_CSV_PATH") according to your dataset csv file
### make sure shape_predictor_68_face_landmarks.dat file is in the same directory as with this script OR change the path in line88
### Change line 111 with the path that shows your dataset file

def get_cropped_mouth_img(detector, predictor, input_image, mouth_margin=6, mouth_size=32):
    gray = cv2.cvtColor(input_image, cv2.COLOR_BGR2GRAY)
    # detect faces in the grayscale image
    rects = detector(gray, 1)
    if len(rects) != 1: # if number of faces is more than 1 or less than 1, discard
        return None
    for (i,rect) in enumerate(rects):
        shape = predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)
        for (name,(i,j)) in face_utils.FACIAL_LANDMARKS_IDXS.items():
            if name == 'mouth':
                (x, y, w, h) = cv2.boundingRect(np.array([shape[i:j]]))
                # check w and h and result squared image  so you dont need to padding and you wont lose information
                if w > h:
                    padding_h_total = w - h
                    if padding_h_total % 2 != 0:
                        padding_h_total += 1
                    padding_h = padding_h_total // 2

                    cropped_mouth = gray[y - (mouth_margin + padding_h):y + h + mouth_margin + padding_h, x - mouth_margin:x + w + mouth_margin]
                    return imutils.resize(cropped_mouth, width=mouth_size, inter=cv2.INTER_CUBIC)
                elif w < h:
                    padding_w_total = h - w
                    if padding_w_total % 2 != 0:
                        padding_w_total += 1
                    padding_w = padding_w_total // 2
                    cropped_mouth = gray[y - mouth_margin:y + h + mouth_margin, x - (mouth_margin + padding_w):x + w + mouth_margin + padding_w]
                    return imutils.resize(cropped_mouth, width=mouth_size, inter=cv2.INTER_CUBIC)
                else:
                    cropped_mouth = gray[y - mouth_margin:y + h + mouth_margin, x - mouth_margin:x + w + mouth_margin]
                    return imutils.resize(cropped_mouth, width=mouth_size, inter=cv2.INTER_CUBIC)
    return None


def get_mouth_frames_from_video(detector, predictor, video_input_path, mouth_margin=6, mouth_size=32):
    # Opens the Video file
    mouth_frames_list = []
    cap = cv2.VideoCapture(video_input_path)
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == False:
            break
        mouth_frame = get_cropped_mouth_img(detector, predictor, frame, mouth_margin, mouth_size)
        if mouth_frame is not None:
            mouth_frames_list.append(mouth_frame)
    cap.release()
    return mouth_frames_list

def merge_mouth_imgs(mouth_img_list, dataset_item_size=224, mouth_size=32): # NOTE mouth_list is a list contains cv2 images which are 32x32 mouth imgs
    seq = np.zeros((dataset_item_size, dataset_item_size))
    mouth_img_list_size = len(mouth_img_list)
    if mouth_img_list_size == 0:
        return None
    x_limit = mouth_size
    y_limit = mouth_size
    iterator_x = 0
    iterator_y = 0
    num_of_tot_frames = (dataset_item_size // mouth_size) * (dataset_item_size // mouth_size)
    for i in range(0, num_of_tot_frames):
        placement_mouth = mouth_img_list[int((i*mouth_img_list_size)/num_of_tot_frames)]
        if placement_mouth.shape[0] != mouth_size or placement_mouth.shape[1] != mouth_size:
            placement_mouth = cv2.resize(placement_mouth,(32,32),interpolation = cv2.INTER_LINEAR)
        seq[iterator_y:iterator_y + y_limit, iterator_x:iterator_x + x_limit] =  placement_mouth # movement along y-axis
        iterator_x = iterator_x + x_limit
        if iterator_x == dataset_item_size:
            iterator_x = 0
            iterator_y = iterator_y + y_limit 
    return seq

def video_to_image(vid_queue):
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
    while True:
        vid = vid_queue.get()
        if vid == None:
            break
        dataset_final_img = merge_mouth_imgs(get_mouth_frames_from_video(detector, predictor, vid))
        if dataset_final_img is not None:   
            destination = vid.split(os.sep)[-2] + os.sep + "processed"
            frameFinalName = "img_" + vid.split(os.sep)[-1][:-4] + ".png"
            script_path = os.getcwd()
            os.chdir(destination)
            mpimg.imsave(frameFinalName, dataset_final_img, cmap="gray")
            os.chdir(script_path)

if __name__ == '__main__':
    dataset_label_folders_set = set()

    with open('DATASET_CSV_PATH') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                dataset_label_folders_set.add(row[1])
                line_count += 1

    dataset_label_folders = list(dataset_label_folders_set)

    parser = argparse.ArgumentParser()

    parser.add_argument('--batch-size', nargs='?', const=224, type=int,
        help="Define the size of batch, e.g 224 or 256")

    parser.add_argument('--batch-item-size', nargs='?', const=32, type=int,
        help="Define the size of each item in batch, e.g 32 or 48")

    args = parser.parse_args()

    dataset_batch_size = args.batch_size
    dataset_batch_item_size = args.batch_item_size

    print("batch size: " + str(dataset_batch_size))
    print("batch item size: " + str(dataset_batch_item_size))

    # initialize dlib's face detector (HOG-based) and then create
    # the facial landmark predictor
    
    # make folders
    for label_folder in dataset_label_folders:
        target_dir = os.getcwd() + os.sep + label_folder + os.sep + "processed"
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

    all_video_path = []
    for label_folder in dataset_label_folders:
        label_dir = os.getcwd() + os.sep + label_folder
        for each_video in os.listdir(label_dir):
            if each_video.endswith(".mp4"):
                all_video_path.append(label_dir + os.sep + each_video)

    NUM_PROC = 44
    vid_queue = mp.Queue(maxsize=NUM_PROC)
    
    vid_pool = mp.Pool(NUM_PROC, video_to_image, (vid_queue,))
    for vid in tqdm(all_video_path):
        vid_queue.put(vid)

    for i in range(NUM_PROC):
        vid_queue.put(None)
    vid_pool.close()
    vid_pool.join()
    print("Finished...")
