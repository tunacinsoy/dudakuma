from __future__ import unicode_literals
from distutils.log import error
import sys
import os.path
import re
import glob
import csv
from datetime import datetime
import time
import string
import random

from numpy import empty

### Edit line70 to line79 according to your labels/words, and edit 'label_max_count' in line59 according to your label/class utterances number
### Make sure all the downloaded subtitles(.vtt files) are on the same working directory as this script

def get_url_from_filename(filename):
    url = filename[:-len('.tr.vtt')]
    url = url[len(url)-11:]
    url = "https://www.youtube.com/watch?v=" + url
    return url

def get_predicted_timerange(word, sentence, sentence_start_time, sentence_end_time):

    start_t = datetime.strptime(('01.01.2022 '+sentence_start_time),"%d.%m.%Y %H:%M:%S.%f").timestamp()
    end_t = datetime.strptime(('01.01.2022 '+sentence_end_time),"%d.%m.%Y %H:%M:%S.%f").timestamp()
    duration =  (end_t - start_t)

    sentence2 = sentence.lstrip().lower()
    translator = str.maketrans(string.punctuation, ' '*len(string.punctuation)) #map punctuation to space
    cleaned_sentence = sentence2.translate(translator)
    word_list = cleaned_sentence.split()
    char_count = sum(len(i) for i in word_list)
    cap_vovel_count = sum(sum( 1 for k in i if k in "aeiıoöuü") for i in word_list)
    
    word_start_t = start_t
    for eachword in word_list:
        vovel_count = sum(1 for k in eachword if k in "aeiıoöuü")

        word_end_t = word_start_t + duration*(vovel_count/cap_vovel_count)
        #print("word_end_t",word_end_t , "word_start_t ",word_start_t, "duration " , duration , "vovel_count ",vovel_count,"cap_vovel_count ",cap_vovel_count)
        if eachword == word:
            
            predicted_start_time = datetime.fromtimestamp(word_start_t).strftime('%H:%M:%S.%f')
            predicted_end_time = datetime.fromtimestamp(word_end_t).strftime('%H:%M:%S.%f')
            result_dict = {
                "start": predicted_start_time,
                "end": predicted_end_time
            }
            #print("Girdi ",result_dict)
            return result_dict
        word_start_t = word_end_t

def sentence_contain_word(sentence, word):
    sentence2 = sentence.lstrip().lower().strip()
    translator = str.maketrans(string.punctuation, ' '*len(string.punctuation)) #map punctuation to space
    cleaned_sentence = sentence2.translate(translator)
    cleaned_sentence_word_arr = cleaned_sentence.split()

    for a in cleaned_sentence_word_arr:
        if a.lower().__eq__(word.lower()):
            return True
        else:
            return False    
    """if word in cleaned_sentence_word_arr:
        return True
    else:
        return False"""

def main(argv):
    label_max_count = 500
    word1arr = []
    word2arr = []
    word3arr = []
    word4arr = []
    word5arr = []
    word6arr = []
    word7arr = []
    word8arr = []
    word9arr = []
    word10arr = []
    labelword1 = "hayat"
    labelword2 = "ilgili"
    labelword3 = "şimdi"
    labelword4 = "sürekli"
    labelword5 = "içerisinde"
    labelword6 = "kendi"
    labelword7 = "olabilir"
    labelword8 = "doğru"
    labelword9 = "istiyorum"
    labelword10 = "gerçekten"
    all_sentences_list = []
    for file in glob.glob("PATH_OF_VTT_FILES/*.vtt"):
        # subtitle has been downloaded succesfully
        ##### PROCESSING SUBTITLE FILE PART #####
        file1 = open(file, 'r',encoding="utf-8")
        try:
           sbt_lines = file1.readlines()
        except:
            print("HATAAAAAAAAAAAAAAAAAAAAAAAA")
        file1.close()
        
        vtt_pattern = re.compile("(?m)^(\d{2}:\d{2}:\d{2}\.\d+) +--> +(\d{2}:\d{2}:\d{2}\.\d+)")
        found_vtt_timestamp = False
        vtt_timestamp_start = None
        vtt_timestamp_end = None
        
        for line in sbt_lines:
            if found_vtt_timestamp:
                found_vtt_timestamp = False
                caption = {
                "video_url": get_url_from_filename(file),
                "start": vtt_timestamp_start,
                "end": vtt_timestamp_end,
                "text": line
                }
                if len(line.strip()) == 0:
                    continue
                all_sentences_list.append(caption)
                continue
            result = vtt_pattern.match(line)
            
            if result:
                found_vtt_timestamp = True
                vtt_timestamp_start = result.group(1)
                vtt_timestamp_end = result.group(2)
            else:
                continue
    
    random.shuffle(all_sentences_list) # shuffle list for more and more randomized dataset
    for subtitle_part in all_sentences_list:        
        try:
            if sentence_contain_word(subtitle_part['text'], labelword1):
                if len(word1arr) < label_max_count:
                    predicted_timerange = get_predicted_timerange(labelword1, subtitle_part['text'].strip(), subtitle_part['start'], subtitle_part['end'])
                    predicted_timerange_start = predicted_timerange['start']
                    predicted_timerange_end = predicted_timerange['end']
                    result_dictionary = {
                    "video_url": subtitle_part['video_url'],
                    "start": predicted_timerange_start,
                    "end": predicted_timerange_end,
                    "label": labelword1
                    }
                    word1arr.append(result_dictionary)
                else:
                    continue
            if sentence_contain_word(subtitle_part['text'], labelword2):
                if len(word2arr) < label_max_count:
                    predicted_timerange = get_predicted_timerange(labelword2, subtitle_part['text'], subtitle_part['start'], subtitle_part['end'])
                    predicted_timerange_start = predicted_timerange['start']
                    predicted_timerange_end = predicted_timerange['end']
                    result_dictionary = {
                    "video_url": subtitle_part['video_url'],
                    "start": predicted_timerange_start,
                    "end": predicted_timerange_end,
                    "label": labelword2
                    }
                    word2arr.append(result_dictionary)
                else:
                    continue
            
            if sentence_contain_word(subtitle_part['text'], labelword3):
                if len(word3arr) < label_max_count:
                    predicted_timerange = get_predicted_timerange(labelword3, subtitle_part['text'], subtitle_part['start'], subtitle_part['end'])
                    predicted_timerange_start = predicted_timerange['start']
                    predicted_timerange_end = predicted_timerange['end']
                    result_dictionary = {
                    "video_url": subtitle_part['video_url'],
                    "start": predicted_timerange_start,
                    "end": predicted_timerange_end,
                    "label": labelword3
                    }
                    word3arr.append(result_dictionary)
                else:
                    continue
            if sentence_contain_word(subtitle_part['text'], labelword4):
                if len(word4arr) < label_max_count:
                    predicted_timerange = get_predicted_timerange(labelword4, subtitle_part['text'], subtitle_part['start'], subtitle_part['end'])
                    predicted_timerange_start = predicted_timerange['start']
                    predicted_timerange_end = predicted_timerange['end']
                    result_dictionary = {
                    "video_url": subtitle_part['video_url'],
                    "start": predicted_timerange_start,
                    "end": predicted_timerange_end,
                    "label": labelword4
                    }
                    word4arr.append(result_dictionary)
                else:
                    continue
            if sentence_contain_word(subtitle_part['text'], labelword5):
                if len(word5arr) < label_max_count:
                    predicted_timerange = get_predicted_timerange(labelword5, subtitle_part['text'], subtitle_part['start'], subtitle_part['end'])
                    predicted_timerange_start = predicted_timerange['start']
                    predicted_timerange_end = predicted_timerange['end']
                    result_dictionary = {
                    "video_url": subtitle_part['video_url'],
                    "start": predicted_timerange_start,
                    "end": predicted_timerange_end,
                    "label": labelword5
                    }
                    word5arr.append(result_dictionary)
                else:
                    continue
            if sentence_contain_word(subtitle_part['text'], labelword6):
                if len(word6arr) < label_max_count:
                    predicted_timerange = get_predicted_timerange(labelword6, subtitle_part['text'], subtitle_part['start'], subtitle_part['end'])
                    predicted_timerange_start = predicted_timerange['start']
                    predicted_timerange_end = predicted_timerange['end']
                    result_dictionary = {
                    "video_url": subtitle_part['video_url'],
                    "start": predicted_timerange_start,
                    "end": predicted_timerange_end,
                    "label": labelword6
                    }
                    word6arr.append(result_dictionary)
                else:
                    continue
            if sentence_contain_word(subtitle_part['text'], labelword7):
                if len(word7arr) < label_max_count:
                    predicted_timerange = get_predicted_timerange(labelword7, subtitle_part['text'], subtitle_part['start'], subtitle_part['end'])
                    predicted_timerange_start = predicted_timerange['start']
                    predicted_timerange_end = predicted_timerange['end']
                    result_dictionary = {
                    "video_url": subtitle_part['video_url'],
                    "start": predicted_timerange_start,
                    "end": predicted_timerange_end,
                    "label": labelword7
                    }
                    word7arr.append(result_dictionary)
                else:
                    continue
            if sentence_contain_word(subtitle_part['text'], labelword8):
                if len(word8arr) < label_max_count:
                    predicted_timerange = get_predicted_timerange(labelword8, subtitle_part['text'], subtitle_part['start'], subtitle_part['end'])
                    predicted_timerange_start = predicted_timerange['start']
                    predicted_timerange_end = predicted_timerange['end']
                    result_dictionary = {
                    "video_url": subtitle_part['video_url'],
                    "start": predicted_timerange_start,
                    "end": predicted_timerange_end,
                    "label": labelword8
                    }
                    word8arr.append(result_dictionary)
                else:
                    continue
            if sentence_contain_word(subtitle_part['text'], labelword9):
                if len(word9arr) < label_max_count:
                    predicted_timerange = get_predicted_timerange(labelword9, subtitle_part['text'], subtitle_part['start'], subtitle_part['end'])
                    predicted_timerange_start = predicted_timerange['start']
                    predicted_timerange_end = predicted_timerange['end']
                    result_dictionary = {
                    "video_url": subtitle_part['video_url'],
                    "start": predicted_timerange_start,
                    "end": predicted_timerange_end,
                    "label": labelword9
                    }
                    word9arr.append(result_dictionary)
                else:
                    continue
            if sentence_contain_word(subtitle_part['text'], labelword10):
                if len(word10arr) < label_max_count:
                    predicted_timerange = get_predicted_timerange(labelword10, subtitle_part['text'], subtitle_part['start'], subtitle_part['end'])
                    predicted_timerange_start = predicted_timerange['start']
                    predicted_timerange_end = predicted_timerange['end']
                    result_dictionary = {
                    "video_url": subtitle_part['video_url'],
                    "start": predicted_timerange_start,
                    "end": predicted_timerange_end,
                    "label": labelword10
                    }
                    word10arr.append(result_dictionary)
                else:
                    continue
        except Exception as e:
            print("Oops!", e, "occurred.")
            """print("*****************\nHATA LİNE 274")
            print("text", subtitle_part['text'])
            print("start",subtitle_part['start'])
            print("end",subtitle_part['end']+ "\n*****************\n")"""
    # write to dataset
    dataset3_file = open("dataset.csv", "w")
    dataset3_writer = csv.writer(dataset3_file)
    dataset3_writer.writerow(["video_url", "label", "start_time", "end_time"])
    for each_labeled_data in word1arr:
        dataset3_writer.writerow([each_labeled_data['video_url'], each_labeled_data['label'], each_labeled_data['start'], each_labeled_data['end']])

    for each_labeled_data in word2arr:
        dataset3_writer.writerow([each_labeled_data['video_url'], each_labeled_data['label'], each_labeled_data['start'], each_labeled_data['end']])

    for each_labeled_data in word3arr:
        dataset3_writer.writerow([each_labeled_data['video_url'], each_labeled_data['label'], each_labeled_data['start'], each_labeled_data['end']])

    for each_labeled_data in word4arr:
        dataset3_writer.writerow([each_labeled_data['video_url'], each_labeled_data['label'], each_labeled_data['start'], each_labeled_data['end']])

    for each_labeled_data in word5arr:
        dataset3_writer.writerow([each_labeled_data['video_url'], each_labeled_data['label'], each_labeled_data['start'], each_labeled_data['end']])

    for each_labeled_data in word6arr:
        dataset3_writer.writerow([each_labeled_data['video_url'], each_labeled_data['label'], each_labeled_data['start'], each_labeled_data['end']])

    for each_labeled_data in word7arr:
        dataset3_writer.writerow([each_labeled_data['video_url'], each_labeled_data['label'], each_labeled_data['start'], each_labeled_data['end']])

    for each_labeled_data in word8arr:
        dataset3_writer.writerow([each_labeled_data['video_url'], each_labeled_data['label'], each_labeled_data['start'], each_labeled_data['end']])

    for each_labeled_data in word9arr:
        dataset3_writer.writerow([each_labeled_data['video_url'], each_labeled_data['label'], each_labeled_data['start'], each_labeled_data['end']])

    for each_labeled_data in word10arr:
        dataset3_writer.writerow([each_labeled_data['video_url'], each_labeled_data['label'], each_labeled_data['start'], each_labeled_data['end']])

    dataset3_file.close()
if __name__ == "__main__":
    main(sys.argv)
